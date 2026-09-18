"""Ask questions about a database in plain language; the agent writes the SQL."""

import os
import sqlite3
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq

load_dotenv()

DB_FILE = "erp_mock.db"
MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """\
You are an assistant embedded in an ERP system.
Answer the user's question by writing and running SQLite queries.

List the tables and read their schema before writing a query.
An invoice is overdue when status = 'Overdue'.
Never modify data: SELECT only.
Answer in business language, not SQL.
"""

CUSTOMERS = [
    (1, "TechCorp", "Poland", 50000),
    (2, "GlobalLogistics", "Germany", 120000),
    (3, "RetailPlus", "UK", 30000),
]

INVOICES = [
    (101, 1, 4500.00, "2026-09-01", "Overdue"),
    (102, 1, 1200.50, "2026-09-25", "Pending"),
    (103, 2, 15000.00, "2026-08-15", "Overdue"),
    (104, 3, 850.00, "2026-10-10", "Pending"),
]


def init_mock_db(path: str = DB_FILE) -> None:
    """Build a throwaway SQLite stand-in for an ERP finance module."""
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id  INTEGER PRIMARY KEY,
                name         TEXT,
                country      TEXT,
                credit_limit REAL
            );
            CREATE TABLE IF NOT EXISTS Invoices (
                invoice_id  INTEGER PRIMARY KEY,
                customer_id INTEGER REFERENCES Customers(customer_id),
                amount      REAL,
                due_date    TEXT,
                status      TEXT
            );
            DELETE FROM Customers;
            DELETE FROM Invoices;
        """)
        conn.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?)", CUSTOMERS)
        conn.executemany("INSERT INTO Invoices VALUES (?, ?, ?, ?, ?)", INVOICES)

    print(f"Mock ERP database ready: {path}")


def build_agent(db_file: str = DB_FILE):
    """Wire the model to the database and return a ready agent."""
    db = SQLDatabase.from_uri(f"sqlite:///{db_file}")
    llm = ChatGroq(model=MODEL, temperature=0)  # reads GROQ_API_KEY from the env
    tools = SQLDatabaseToolkit(db=db, llm=llm).get_tools()

    print("Tools available to the agent:", [t.name for t in tools])
    return create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)


def show_tool_calls(messages) -> None:
    """Print each tool the agent decided to call, so the loop is not a black box."""
    for message in messages:
        for call in getattr(message, "tool_calls", None) or []:
            args = ", ".join(f"{k}={v!r}" for k, v in call["args"].items())
            print(f"  -> {call['name']}({args})")


def main() -> None:
    # Windows consoles default to a legacy codepage; model output is UTF-8.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if not os.getenv("GROQ_API_KEY"):
        raise SystemExit("Set GROQ_API_KEY in .env (free key from console.groq.com)")

    init_mock_db()
    agent = build_agent()

    print("Ask a question, or 'exit' to quit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit", ""}:
            break

        result = agent.invoke({"messages": [("human", question)]})
        show_tool_calls(result["messages"])
        print(f"\nAgent: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()
