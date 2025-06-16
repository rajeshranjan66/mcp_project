from dotenv import load_dotenv
from fastmcp import FastMCP
from langchain_community.tools.tavily_search import TavilySearchResults
import os

load_dotenv()

# Define freshness_hours (e.g., from an environment variable or as a constant)
#freshness_hours = os.getenv("FRESHNESS_HOURS", "1")  # Default to 24 hours if not set

mcp = FastMCP("WebCrawlerMCP", "1.0.0", "A server to crawl web pages and extract data using Tavli API.")

@mcp.tool()
def crawl_web_page(query: str, freshness_hours: int = 1) -> dict:
    """
    Crawl a web page or perform a search using the Tavily API.
    Args:
        query (str): The search query or URL to crawl.
    Returns:
        dict: The search results or extracted content.
    """
    try:

        search = TavilySearchResults(max_results=3)
        return search.invoke({
            "query": query,
            "freshness": f"{freshness_hours}h"
        })
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
