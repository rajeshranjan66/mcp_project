import asyncio
from pprint import pprint
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Initialize the chat model
model = init_chat_model("gpt-4o")
#model=ChatGoogleGenerativeAI(model='gemini-1.5-flash')

# Define multiple MCP servers
server_params = {
    "stocksAnalysisMCPServer": {
        "command": "python",
        "args": ["/Users/rajeshranjan/RajeshWork/mcp/mcp_project/mcp_server/mcp_stock_server.py"],
        "transport": "stdio",
    },
    "WebCrawlerMCP": {
        "command": "python",
        "args": ["/Users/rajeshranjan/RajeshWork/mcp/mcp_project/mcp_server/mcp_webcrawler_server.py"],
        "transport": "stdio",
    }
}


async def main():
    client = MultiServerMCPClient(server_params)
    tools = await client.get_tools()

    def call_model(state: MessagesState):
        response = model.bind_tools(tools).invoke(state["messages"])
        # print("-" * 50)
        # print("call model response :", response)
        return {"messages": response}

    # def router_function(state: MessagesState):
    #     message = state["messages"]
    #     last_message = message[-1]
    #     if last_message.tool_calls:
    #         return "tools"
    #     return END


    # Create the state graph
    builder = StateGraph(MessagesState)
    builder.add_node("LLM_Call_with_Tool",call_model)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "LLM_Call_with_Tool")

    builder.add_conditional_edges("LLM_Call_with_Tool",tools_condition)
    builder.add_edge("tools", "LLM_Call_with_Tool")
    app = builder.compile()
    pprint(app)


    #comprehensive_prompt="Should I invest in NVIDIA?"
    comprehensive_prompt = """Perform a complete market and news analysis for Tesla (TSLA):
        1. Get current stock price and today's trading range
        2. Find and analyze the latest 5 news articles about Tesla
        3. Specifically look for:
           - Manufacturing updates
           - Competition news
           - Market expansion news
           - Technology developments
        4. Analyze how each news category affects the stock price
        5. Compare Tesla's performance with industry trends
        6. Summarize:
           - Current market position
           - News sentiment analysis
           - Potential market movers
           - Overall outlook
        Please provide detailed analysis combining both stock data and news context."""
    agent_response = await app.ainvoke({
        "messages": comprehensive_prompt
    },{ "recursion_limit": 5 })
    #agent_response = await app.ainvoke({"messages": " find 3+3 and explain and summarize explaination"})
    #agent_response = await app.ainvoke({"messages": "Find the current stock prices of MSFT and AAPL, then compare their performance and explain which might be a better investment based on current market trends"})
    #agent_response = await app.ainvoke({"messages": "what is the current price of MSFT, Fetch the stock price history of MSFT for the last month and analyze the trend."})
    #agent_response = await app.ainvoke({"messages": "what is the current price of MSFT?"})
    print("*" * 100)
    #print(f"Over all resposne : {agent_response}")
    #print("*" * 100)
    #messages = agent_response  # Your message dictionary
    for m in agent_response['messages']:
        m.pretty_print()



if __name__ == "__main__":
    asyncio.run(main())
