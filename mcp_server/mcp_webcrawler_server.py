from dotenv import load_dotenv
from fastmcp import FastMCP
from langchain_community.tools.tavily_search import TavilySearchResults


load_dotenv()

mcp = FastMCP("WebCrawlerMCP", "1.0.0", "A server to crawl web pages and extract data using Tavli API.")

@mcp.tool()
def crawl_web_page(query: str) -> dict:
    """
    Crawl a web page or perform a search using the Tavily API.
    Args:
        query (str): The search query or URL to crawl.
    Returns:
        dict: The search results or extracted content.
    """
    try:
        # Initialize TavilySearchResults with a maximum of 3 results
        search = TavilySearchResults(max_results=3)
        # Perform the search using the query
        search_results = search.invoke(query)
        # Return the search results
        return {"query": query, "results": search_results}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")

