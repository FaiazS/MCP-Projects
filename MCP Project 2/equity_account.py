import json

from datetime import datetime

from dotenv import load_dotenv

from pydantic import BaseModel

from equity_market import get_company_equity_stock_price

from equity_database import register_equity_account, get_equity_account, update_equity_database_log

load_dotenv(override=True)

OPENING_BALANCE = 10000.00

SPREAD = 0.002

class EquityTransaction(BaseModel):

    stock_symbol: str

    stock_quantity: int

    stock_price: float

    transaction_timestamp: str

    rationale: str

    def stock_total_price(self) -> float:

        return self.stock_quantity * self.stock_price
    
    def __repr__(self):

        return f"{abs(self.stock_quantity)} stocks of {self.stock_symbol} at {self.stock_price} each."


class EquityAccount(BaseModel):

  account_name: str

  account_balance: float

  account_transactions: list[EquityTransaction]

  investment_strategy: str

  account_holdings: dict[str, int]

  account_portfolio_value_time_series: list[tuple[str, float]]


  @classmethod
  def get_account_details(cls, account_holder_name: str):
      
      input_fields = get_equity_account(equity_account_name=account_holder_name)

      if not input_fields:
          
          input_fields = {
              
              'account_name' : account_holder_name.lower(),

              'account_balance': OPENING_BALANCE,

              'account_transactions': [],

              'investment_strategy' : '',

              'account_holdings': {},

              'account_portfolio_value_time_series' : []

          }
          register_equity_account(equity_account_name=account_holder_name, equity_account_info=input_fields)

      return cls(**input_fields)
    
  def update_account_details(self):

    register_equity_account(equity_account_name=self.account_name.lower(), equity_account_info=self.model_dump())


  def restart_investment(self, investment_strategy: str):
     
     self.account_balance = OPENING_BALANCE

     self.account_transactions = []

     self.investment_strategy = investment_strategy

     self.account_holdings = {}

     self.account_portfolio_value_time_series = []

     self.update_account_details()


  def deposit_funds(self, amount: float):
     
     if amount <= 0:

        raise ValueError('Please specify a valid amount greater than 0.')

     self.account_balance += amount

     print(f"Added ${amount} to account balance. Updated balance: ${self.account_balance}")

     self.update_account_details()

  def withdraw_funds(self, amount: float):

    if amount > self.account_balance:
       
       raise ValueError(f"Insufficient funds, please try again with an amount lower than current available balance: ${self.account_balance}")
    
    self.account_balance -= amount

    print(f"${amount} withdrawn successfully. Updated balance: ${self.account_balance}")

    self.update_account_details()

 
  def purchase_stock(self, company_symbol: str, stock_quantity: int, rationale: str) -> str:
     
     current_stock_price = get_company_equity_stock_price(company_symbol=company_symbol)

     stock_buy_price = current_stock_price * (1 + SPREAD)

     total_stock_cost = stock_buy_price * stock_quantity

     if total_stock_cost > self.account_balance:

        raise ValueError('Insufficient funds to purchase the requested quantity, please deposit additional funds to complete purchase or reduce the quantity and try again.')
     
     elif current_stock_price == 0:

        raise ValueError('Company symbol is invalid')
     
     self.account_holdings[company_symbol] = self.account_holdings.get(company_symbol, 0) + stock_quantity

     purchase_time = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')

     purchase_transaction_record = EquityTransaction(
        
                                                      stock_symbol = company_symbol, 
                                                     
                                                      stock_quantity = stock_quantity, 
                                                    
                                                      stock_price = stock_buy_price, 

                                                      transaction_timestamp = purchase_time, 

                                                      rationale = rationale
                                                      
                                                      )
     
     self.account_transactions.append(purchase_transaction_record)

     self.account_balance -= total_stock_cost

     self.update_account_details()

     update_equity_database_log(
        
                                log_name = self.account_name, 
                                
                                log_type= 'equity account', 
                                
                                log_message= f"Purchased {stock_quantity} shares of {company_symbol}"
                                
                                )

     return f"Purchase completed with {stock_quantity} shares of {company_symbol} credited to Equity Portfolio." + self.equity_report()
  

  def sell_stock(self, company_symbol: str, stock_quantity: int, rationale: str) -> str:
     
     if stock_quantity > self.account_holdings.get(company_symbol, 0):

        raise ValueError('Stock quantity specified is greater than available quantity, kindly specify within the available quantity.')
     
     current_price = get_company_equity_stock_price(company_symbol = company_symbol)

     sell_price = current_price * (1 - SPREAD)

     total_sale_value = sell_price * stock_quantity

     self.account_holdings[company_symbol] -= stock_quantity

     if self.account_holdings[company_symbol] == 0:

        del self.account_holdings[company_symbol]
    
     sale_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

     sale_transaction_record = EquityTransaction(

                                       stock_symbol= company_symbol,

                                       stock_quantity=stock_quantity,

                                       stock_price=sell_price,

                                       transaction_timestamp= sale_time,

                                       rationale = rationale

     )

     self.account_transactions.append(sale_transaction_record)

     self.account_balance += total_sale_value

     self.update_account_details()

     update_equity_database_log(

                                log_name = self.account_name, 
                                
                                log_type= 'equity account', 
                                
                                log_message= f"Sold {stock_quantity} shares of {company_symbol}"
                                
                                )

     return f"Sale of {stock_quantity} shares of {company_symbol} successful and debited from equity portfolio." + self.equity_report()
  

  def calculate_equity_portfolio_value(self):
     
     total_equity_value = self.account_balance

     for company_symbol, stock_quantity in self.account_holdings.items():

        total_equity_value += get_company_equity_stock_price(company_symbol=company_symbol) * stock_quantity 

     return total_equity_value

  def calculate_equity_profit_and_loss(self, current_market_value):
     
     initial_spending = sum(account_transaction.stock_total_price() for account_transaction in self.account_transactions)

     equity_profit_and_loss = current_market_value - initial_spending - self.account_balance

     return equity_profit_and_loss

  def get_holdings(self):
     
     return self.account_holdings

  def get_equity_profit_and_loss(self):
     
     return self.calculate_equity_profit_and_loss()
  
  def equity_transactions_list(self):
     
     return [account_transaction.model_dump() for account_transaction in self.account_transactions]
  
  def equity_report(self) -> str:
     
     equity_portfolio_value = self.calculate_equity_portfolio_value

     self.account_portfolio_value_time_series.append((datetime.now().strftime('%d/%m/%Y, %H:%M:%S'), equity_portfolio_value))

     self.update_account_details()

     profit_and_loss = self.calculate_equity_profit_and_loss(current_market_value = equity_portfolio_value)

     equity_data = self.model_dump()

     equity_data['equity_portfolio_value'] = equity_portfolio_value

     equity_data['profit_and_loss'] = profit_and_loss

     update_equity_database_log(log_name = self.account_name, 
                                
                                log_type = 'equity account', 
                                
                                log_message = 'Retrieved Equity report')
     
     return json.dumps(equity_data)

     
  def get_investment_strategy(self) -> str:
     
     update_equity_database_log(
                                
                                log_name=self.account_name,

                                log_type= 'equity account',

                                log_message='Retrieved investment strategy'
                                
                                )
     
     return f"Investment Strategy: {self.investment_strategy}"
  

  def update_investment_strategy(self, updated_investment_strategy: str) -> str:
     
     self.investment_strategy = updated_investment_strategy

     self.update_account_details()

     update_equity_database_log(

                               log_name = self.account_name,

                               log_type = 'equity account',

                               log_message = 'Investment strategy updated/modified.'


     )

     return f"Updated investment strategy: {self.investment_strategy}"
  
if __name__ == '__main__':
     
    equity_account = EquityAccount('Faiaz Ahmed')

    equity_account.deposit_funds(500.00)

    equity_account.sell_stock('AAPL', 4)

    equity_account.purchase_stock('AMZN', 7)

    print(f"Current holdings: {equity_account.get_holdings()}")

    print(f"Transaction history: {equity_account.equity_transactions_list()}")

    print(f"Current Profit & Loss: {equity_account.get_equity_profit_and_loss()}")

    print(f"Current portfolio value:{equity_account.calculate_equity_portfolio_value()}")
