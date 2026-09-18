"""sql_agent.py stripped to the lines that matter: one table, one question, no loop."""

import sqlite3
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq

load_dotenv()
# Model outputs UTF-8 (special spaces and quote marks); cp1250 console would crash.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_FILE = "minimal.db"
QUESTION = "Which invoices are overdue, and how much do they come to in total?"


def show_tool_calls(messages):
    """Walk the message list and print every tool the model asked for."""
    for message in messages:
        for call in getattr(message, "tool_calls", None) or []:
            print(f"  -> {call['name']}({call['args']})")


# One-table rebuilt each run.
with sqlite3.connect(DB_FILE) as conn:
    conn.execute("DROP TABLE IF EXISTS Invoices")
    conn.execute("CREATE TABLE Invoices (customer TEXT, amount REAL, status TEXT)")
    conn.executemany("INSERT INTO Invoices VALUES (?, ?, ?)", [
        ("TechCorp", 4500.00, "Overdue"),
        ("GlobalLogistics", 15000.00, "Overdue"),
        ("RetailPlus", 850.00, "Pending"),
    ])

# --- the agent -----------------------------------------------------------
db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE}")
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
tools = SQLDatabaseToolkit(db=db, llm=llm).get_tools()
agent = create_agent(llm, tools, system_prompt="Answer the question by querying the database. SELECT only.")

# Agentic loop is inside invoke()
result = agent.invoke({"messages": [("human", QUESTION)]})
# -------------------------------------------------------------------------

# The model picked these tools, in this order. Nothing here told it to.
show_tool_calls(result["messages"])

print(f"\nQuestion: {QUESTION}")
print(f"Answer: {result['messages'][-1].content}")
