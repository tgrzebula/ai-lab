# ai-lab

A public notebook of my AI experiments — small, self-contained projects I build while
learning. 
## Experiments

| # | Experiment | What it is | Stack |
|---|------------|------------|-------|
| 01 | [GPT Hello World (2024)](01_gpt_hello_world_2024/) | First contact with the OpenAI API — chat completions, embeddings, image generation | Python, `openai` |
| 02 | [RAG and first agents (2025)](02_rag_and_first_agents_2025/) | A minimal RAG pipeline, and the same ReAct agent on two generations of the LangChain API | LlamaIndex, LangChain |
| 03 | [LangGraph agents (2025)](03_langgraph_agents_2025/) | The agent from 02 rebuilt on LangGraph | LangGraph |
| 04 | [SQL agent (2026)](04_sql_agent_2026/) | An agent that answers questions about a mock ERP database by writing its own SQL | LangChain `create_agent`, Groq, SQLite |

Experiments 02 and 03 answer the same question — *the square root of the population of
the country that won the 2023 Rugby World Cup* — across three generations of API, which
is the easiest way to see what actually changed.
