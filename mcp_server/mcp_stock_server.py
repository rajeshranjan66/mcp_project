import yfinance as yf
from dotenv import load_dotenv
from fastmcp import FastMCP
from pandas import DataFrame

load_dotenv()

mcp = FastMCP("stocksAnalysisMCPServer", "1.0.0", "A server to analyze stock data using yfinance")

@mcp.tool()
def fetch_stock_info(symbol: str) -> dict:
    """Get Company's general information.
    Args:
        ""symbol (str): Stock symbol of the company.
        Returns:
            "dict": A dictionary containing the company's general information.
    """

    stock = yf.Ticker(symbol)
    return stock.info

@mcp.tool()
def fetch_quarterly_financials(symbol: str) -> DataFrame :
    """Get stock quarterly financials.
    Args:
        symbol (str): Stock symbol of the company.
        Returns:
            ""DataFrame": A DataFrame containing the company's quarterly financials.
    """
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

@mcp.tool()
def fetch_annual_financials(symbol: str) -> DataFrame:
    """Get stock annual financials.
    Args:
        symbol (str): Stock symbol of the company.
        Returns:
            DataFrame: A DataFrame containing the company's annual financials.
    """

    stock = yf.Ticker(symbol)
    return stock.financials.T

@mcp.tool()
def get_stock_price(symbol: str) -> float:
    """Get the latest trading price (regular market price)
    Args:
        symbol (str): Stock symbol of the company.
        Returns:
            float: The current stock price.
    """
    ticker = yf.Ticker(symbol)
    current_price = ticker.info["regularMarketPrice"]
    return float(current_price)
@mcp.tool()
def get_stock_history(symbol: str, period: str = "1mo") -> DataFrame:
    """Get stock price history for a given period.
    Args:
        symbol (str): Stock symbol of the company.
        period (str): The period for which to fetch the stock history (default: "1mo").
        Returns:
            DataFrame: A DataFrame containing the stock price history.
    """

    ticker = yf.Ticker(symbol)
    history = ticker.history(period=period)
    print(f"\n History from MCP server :{history}")
    return history
if __name__ == "__main__":
    mcp.run(transport="stdio")
