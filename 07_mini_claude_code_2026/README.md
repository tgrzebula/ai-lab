# Mini Claude Code

A coding agent in one small file: three tools, a system prompt and a loop. The model
writes `tool: read_file({"path": "calc.py"})` as plain text and the script parses it.


Inspired by Mihail Eric's lecture
[How to code Claude Code in ~200 lines of code](https://www.youtube.com/watch?v=s7ZzkdvCMDY)
in Stanford's CS146S: The Modern Software Developer.

```bash
pip install -r requirements.txt
copy .env.example .env      # then put your API key in .env
python mini_claude_code.py
```
