from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import numexpr

# Modern model
llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(numexpr.evaluate(expression.strip()))
    except:
        return "Calculation error"

# Tools
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [wikipedia, calculator]

# Modern LangGraph agent
agent = create_react_agent(llm, tools)

question = "What is the square root of the population of the country that won the 2023 Rugby World Cup?"

result = agent.invoke({"messages": [("human", question)]})
print(result["messages"][-1].content)