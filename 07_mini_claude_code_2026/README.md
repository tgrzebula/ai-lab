# Mini Claude Code

A coding agent in one small file: three tools, a system prompt and a loop. The model
writes `tool: read_file({"path": "calc.py"})` as plain text and the script parses it
itself, without the API's built-in tool support.

```bash
pip install -r requirements.txt
copy .env.example .env      # then put your API key in .env
python mini_claude_code.py
```
