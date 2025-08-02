from mcp.server.fastmcp import FastMCP

from equity_market import get_equity_price

equity_market_server = FastMCP('equity_market_mcp_server')

@equity_market_server.tool()
def fetch_equity_price(company_symbol: str) -> float:

    return get_equity_price(company_symbol = company_symbol)


if __name__ == '__main__':

    equity_market_server.run(transport= 'stdio')

