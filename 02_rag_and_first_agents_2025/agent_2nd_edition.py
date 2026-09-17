from dotenv import load_dotenv
load_dotenv()
from langchain.agents import load_tools, create_react_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = create_react_agent(llm, tools, prompt=hub.pull("hwchase17/react"))

question = "What is the square root of the population of the country that won the 2023 Rugby World Cup?"
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": question})
