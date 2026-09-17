# 03 — LangGraph agents (2025)

The agent from [`../02_rag_and_first_agents_2025`](../02_rag_and_first_agents_2025) once
more, this time on LangGraph — third generation of the same code from *Developing Apps
with GPT-4 and ChatGPT* (Caelen & Blete, O'Reilly).

`langgraph_agent.py` asks the same question: *the square root of the population of the
country that won the 2023 Rugby World Cup*. The graph runs the ReAct loop itself, so
there is no `AgentExecutor` and no prompt to pull from the hub. Tools are Wikipedia and
a `numexpr` calculator; the model is `gpt-4o-mini` instead of the book's `gpt-3.5-turbo`.

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python langgraph_agent.py
```
