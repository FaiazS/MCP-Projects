import gradio as gr

from user_interface_utils import css, js, Color

from equity_database import get_equity_database_log_entries

from equity_account import EquityAccount

import pandas as pd

import plotly.express as px

import plotly.graph_objs as go

from trading_arena import trader_agents_firstnames, trader_agents_lastnames, short_model_names

component_color_mapper = {

    'trace' :  Color.WHITE,

    'agent' : Color.CYAN,

    'function' : Color.GREEN,

    'generation' : Color.YELLOW,

    'response' : Color.MAGENTA,

    'account' : Color.RED

}

class EquityTrader:

    def __init__(self, name, lastname, model_name):

        self.name = name

        self.lastname = lastname

        self.model_name = model_name

        self.equity_account = EquityAccount.get_account_details(account_holder_name = name)

    def reload_equity_account(self):

        self.equity_account = EquityAccount.get_account_details(self.name)

    def equity_account_title(self):

        return f"<div style= 'text-align:center;font-size:34px;'>{self.name}<span style = 'color:#ccc;font-size:24px;'>({self.model_name}) - {self.lastname}</span></div>"
    
    def get_investment_strategy(self):

        return EquityAccount.get_investment_strategy()
    
    def equity_portfolio_value_dataframe_format(self) -> pd.DataFrame:

        equity_portfolio_dataframe = pd.DataFrame(self.equity_account.account_portfolio_value_time_series, columns = ['Datetime', 'Equity portfolio value'])

        equity_portfolio_dataframe['Datetime'] = pd.to_datetime(equity_portfolio_dataframe['Datetime'])

        return equity_portfolio_dataframe
    
    def equity_portfolio_value_chart_format(self):

        equity_portfolio_value_dataframe = self.equity_portfolio_value_dataframe_format()

        plot_chart= px.line(data_frame = equity_portfolio_value_dataframe, x = equity_portfolio_value_dataframe['Datetime'], y = equity_portfolio_value_dataframe['Equity portfolio value'])

        plot_margin = dict(l = 40, r = 20, t = 20, b = 40)

        plot_chart.update_layout(

            height = 300,

            margin = plot_margin,

            xaxis_title = None,

            yaxis_title = None,

            paper_bgcolor = '#bbb',

            plot_bgcolor = '#dde'
        )

        plot_chart.update_xaxes(tickformat = '%m/%d', tickangle = 45, tickfont = dict(size = 8))

        plot_chart.update_yaxes(tickfont = dict(size = 8), tickformat = ',.0f')

        return plot_chart

    def equity_portfolio_holdings_dataframe_format(self) -> pd.DataFrame:

        equity_holdings = self.equity_account.account_holdings

        if not equity_holdings:

            return pd.DataFrame(columns = ['Equity Symbol', 'Equity Quantity'])

        equity_holdings_dataframe = pd.DataFrame({'Equity Symbol': equity_symbol, 'Equity Quantity': equity_quantity} for equity_symbol, equity_quantity in equity_holdings.items())

        return equity_holdings_dataframe
  
    def equity_transactions_dataframe_format(self) -> pd.DataFrame:

        equity_transactions = self.equity_account.account_transactions

        if not equity_transactions:

            return pd.DataFrame(columns = ['Timestamp', 'Equity Symbol', 'Equity Quantity', 'Price', 'Rationale'])
        
        return pd.DataFrame(equity_transactions)
    
    def display_equity_portfolio_value(self) -> str:

        equity_portfolio_value = self.equity_account.calculate_equity_portfolio_value or 0.0

        profit_and_loss = self.equity_account.calculate_equity_profit_and_loss(current_market_value = equity_portfolio_value) or 0.0

        color_display = 'green' if profit_and_loss >= 0.0 else 'red'

        emoji_display = '⬆' if color_display == 'green' else '⬇'

        return f"div style = 'text-align:center;background-color:{color_display};'<span style ='font-size:32px'>${equity_portfolio_value:,.0f}</span><span style = 'font-size:24px'>&nbsp;nbsp:nbsp{emoji_display}&nbsp${profit_and_loss: ,.0f} </span> </div>"
    
    def display_equity_logs(self, previous = None) -> str:

        equity_logs = get_equity_database_log_entries(log_name = self.equity_account.account_name, recent_logs = 10)

        response = ""

        for log in equity_logs:

            timestamp, type, message = log

            color = component_color_mapper.get(type, Color.WHITE).value()

            response += f"<span style='color:{color}'>{timestamp} : [{type}] {message} </span></br>"

        response = f"<div style = 'height:250px;overflow-y:auto;'>{response}</div>"

        if response != previous:

            return response
        
        return gr.update()


class TraderDashboard:

    def __init__(self, trader_agent: EquityTrader):

        self.trader_agent = trader_agent

        self.equity_portfolio_value = None

        self.portfolio_chart = None

        self.equity_holdings_table = None

        self.equity_transactions_table = None


    def build_trader_gradio_dashboard(self):

        with gr.Column():

            gr.HTML(value = self.trader_agent.equity_account_title())

            with gr.Row():

                 self.equity_portfolio_value = gr.HTML(self.trader_agent.display_equity_portfolio_value)

            with gr.Row():

                self.portfolio_chart = gr.Plot(self.trader_agent.equity_portfolio_value_chart_format(), container = False, show_label = False)

            with gr.Row():

                self.equity_log = gr.HTML(self.trader_agent.display_equity_logs)

            with gr.Row():

                self.equity_holdings_table = gr.DataFrame(
                    
                    value = self.trader_agent.equity_portfolio_holdings_dataframe_format, 
                    
                    label = 'Equity portfolio holdings', 
                    
                    headers = ['Equity Symbol', 'Quantity'],  
                    
                    row_count = (5, 'dynamic'), 
                    
                    col_count = 2, 
                    
                    max_height = 300, 
                    
                    elem_classes = ['dataframe-fix-small']
                    
                    )
                
            with gr.Row():

                self.equity_transactions_table = gr.DataFrame(
                    
                    value = self.trader_agent.equity_transactions_dataframe_format, 
                    
                    label = 'Equity Transactions', 
                    
                    headers = ['Timestamp', 'Equity Symbol', 'Equity Quantity', 'Price', 'Rationale'], 
                    
                    row_count = (5, 'dynamic'), 
                    
                    col_count = 5, 
                    
                    max_height = 300, 
                    
                    elem_classes = ['dataframe-fix']
                    
                    )
                
        dashboard_timer = gr.Timer(value = 120)

        dashboard_timer.tick(
            
            fn = self.refresh_trader_gradio_dashboard, 
            
            inputs = [], 
            
            outputs= [
                
                self.equity_portfolio_value, 
                
                self.portfolio_chart, 
                
                self.equity_holdings_table, 
                
                self.equity_transactions_table
                
                ], 

                show_progress = 'hidden',

                queue = False
                
                )
        
        equity_log_timer = gr.Timer(value = 0.5)

        equity_log_timer.tick(

            fn = self.trader_agent.display_equity_logs,

            inputs = self.equity_log,

            outputs = self.equity_log,

            show_progress = 'hidden',

            queue = False
        )
        
    def refresh_trader_gradio_dashboard(self):

        self.trader_agent.reload_equity_account()

        return (

            self.trader_agent.display_equity_portfolio_value(),

            self.trader_agent.equity_portfolio_value_chart_format(),

            self.trader_agent.equity_portfolio_holdings_dataframe_format(),

            self.trader_agent.equity_transactions_dataframe_format()

        )

def build_gradio_user_interface():

    equity_traders = [
        
        EquityTrader(name = firstname, lastname = lastname, model_name = model_name) for firstname, lastname, model_name in zip(trader_agents_firstnames, trader_agents_lastnames, short_model_names)

        ]
    

    equity_trader_dashboard = [
        
        TraderDashboard(trader_agent = equity_trader) for equity_trader in equity_traders
        
        ]

    with gr.Blocks(
        
        title = 'EQUITY TRADING AGENTS', 
        
        css = css, 
        
        js = js, 
        
        theme = gr.themes.Default(primary_hue = 'sky'), 
        
        fill_width = True
        
        ) as trader_agent_user_interface:
            
            with gr.Row():

                for trader_dashboard in equity_trader_dashboard:

                    trader_dashboard.build_trader_gradio_dashboard()

    return trader_agent_user_interface