from mcp.server.fastmcp import FastMCP

from equity_account import EquityAccount

equity_account_mcp_server = FastMCP('equity_account_server')

@equity_account_mcp_server.tool()
async def get_balance(name: str):

    return EquityAccount.get_account_details(account_holder_name=name).account_balance

@equity_account_mcp_server.tool()
async def get_holdings(name: str) -> dict[str, int]:

    return EquityAccount.get_account_details(account_holder_name=name).get_holdings()

@equity_account_mcp_server.tool()
async def purchase_stock(name: str, company_symbol:str, stock_qty: int, rationale:str) -> float:

    return EquityAccount.get_account_details(account_holder_name= name).purchase_stock(company_symbol=company_symbol,stock_quantity=stock_qty, rationale = rationale)

@equity_account_mcp_server.tool()
async def sell_stock(name: str, company_symbol:str, stock_qty: int, rationale):

    return EquityAccount.get_account_details(account_holder_name=name).sell_stock(company_symbol=company_symbol, stock_quantity=stock_qty, rationale=rationale)

@equity_account_mcp_server.tool()
async def update_investment_strategy(name: str, updated_strategy: str) -> str:

    return EquityAccount.get_account_details(account_holder_name=name).update_investment_strategy(updated_investment_strategy=updated_strategy)

@equity_account_mcp_server.resource('equity_account://equity_report/{name}')
async def get_equity_account_data(name: str) -> str:

    return EquityAccount.get_account_details(account_holder_name=name).equity_report()

@equity_account_mcp_server.resource('equity_account://equity_investment_strategy/{name}')
async def get_investment_strategy_details(name: str) -> str:

    return EquityAccount.get_account_details(account_holder_name= name).get_investment_strategy()

if __name__ == '__main__':

    equity_account_mcp_server.run(transport= 'stdio')


