import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("yfinance", stateless_http=True)

@mcp.tool()
async def get_current_price(ticker: str) -> float:
    """
    Get the current stock price of a given ticker symbol using Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        float: The current stock price.
        Example: 100.21
    """
    return yf.Ticker(ticker).info['currentPrice']

@mcp.tool()
async def get_historical_data(ticker: str, period: str = "1mo", interval: str = "1d"):
    """
    Fetch historical stock price data for a given ticker symbol using Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").
        period (str): The time range for the historical data. 
            Accepted values: 
            "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", 
            "5y", "10y", "ytd", "max".
        interval (str): The data granularity within the specified period.
            Accepted values: 
            "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", 
            "1d", "5d", "1wk", "1mo", "3mo".

    Returns:
        pd.DataFrame: Historical stock data including Open, High, Low, Close, 
        Volume, and Dividends (depending on availability).
    """
    return yf.Ticker(ticker).history(period, interval)

@mcp.tool()
async def get_company_info(ticker: str) -> dict:
    """
    Retrieve general company information and metadata using Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        dict: Dictionary of company information.
    """
    return yf.Ticker(ticker).info

@mcp.tool()
async def get_financials(ticker: str):
    """
    Retrieve a company's financial statements (income statement, cash flow statement, 
    and balance sheet) using Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        dict[str, pd.DataFrame]: Dictionary containing:
            - "income_statement": Income statement DataFrame
            - "cashflow": Cash flow statement DataFrame
            - "balance_sheet": Balance sheet DataFrame
    """
    stock = yf.Ticker(ticker)

    return {
        "income_statement": stock.income_stmt,
        "cashflow": stock.cashflow,
        "balance_sheet":stock.balance_sheet
    }

@mcp.tool()
async def get_news(ticker: str) -> list[dict]:
    """
    Retrieve and format recent news articles related to a given stock ticker 
    using Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        list[dict]: A list of simplified news articles, each containing:
            - 'title' (str): Title of the news article
            - 'summary' (str): Short summary of the article
            - 'published_date' (str): Publication datetime in ISO 8601 format
            - 'link' (str): URL to the article
    """
    news = yf.Ticker(ticker).news
    formatted_news = []
    
    for item in news:
        content = item.get("content", {})
        provider = content.get("provider", {})
        
        formatted_news.append({
            "title": content.get("title"),
            "summary": content.get("summary"),
            "published_date": content.get("pubDate"),
            "link": provider.get("url")
        })

    return formatted_news

if __name__ == "__main__":
    mcp.run(transport="streamable-http")