# 02 — RAG and first agents (2025)

Exercises from *Developing Apps with GPT-4 and ChatGPT* (Caelen & Blete, O'Reilly).
The two agent scripts are the same ReAct agent as the book gives it in each edition,
which is why they sit next to each other.

| Script | What it is |
|--------|------------|
| `llama_index_in_10_lines_of_code.py` | Minimal RAG: index `data/`, ask a question about it |
| `agent_1st_edition.py` | ReAct agent on the book's 1st edition API — `initialize_agent`, already deprecated |
| `agent_2nd_edition.py` | Same agent, 2nd edition API — `create_react_agent` + `AgentExecutor` |

Both agents answer the same question: *the square root of the population of the country
that won the 2023 Rugby World Cup* — Wikipedia lookup plus a calculation. Rebuilt again
on LangGraph in [`../03_langgraph_agents_2025`](../03_langgraph_agents_2025).

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python llama_index_in_10_lines_of_code.py     # run from inside this folder
```

`agent_2nd_edition.py` also pulls its prompt from LangChain Hub, so it needs network
access beyond the OpenAI call.
