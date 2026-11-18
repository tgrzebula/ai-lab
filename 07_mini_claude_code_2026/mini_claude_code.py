"""A coding agent in one small file - to see that there is no magic inside.

A coding agent is only three things:
  1. tools      - ordinary Python functions,
  2. a prompt   - telling the model which tools exist and how to ask for one,
  3. a loop     - ask the model; if it asks for a tool, run it and send the result back.

We do not use the API's built-in tool support. The model simply writes a line like
    tool: read_file({"path": "calc.py"})
and this script finds that line, runs the function and replies with the result.

Run it in the folder you want it to work on - it edits files there without asking,
but cannot touch anything outside that folder:
    python mini_claude_code.py
"""

import inspect
import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()  # reads ANTHROPIC_API_KEY from a .env file into the environment

MODEL = "claude-sonnet-5-5"  # a mid-size current model: capable and fairly cheap
FOLDER = Path.cwd().resolve()  # the agent may only work inside this folder

# The system prompt: what the model is told before your first question.
SYSTEM_PROMPT_TEMPLATE = """You are a coding assistant working in the folder {folder}.
You can read, list and edit files with the tools below. You cannot run commands,
and paths outside this folder are refused.

To use a tool, reply with exactly one line in this form and nothing else:
tool: TOOL_NAME({{"argument": "value"}})
The arguments are compact JSON on that single line, with double quotes.

Then stop and wait. The next message will start with tool_result: and contain
what the tool returned. Read a file before you edit it.
When you need no more tools, answer the user normally.

Available tools:

{tools}"""


# ---------------------------------------------------------------------------
# Part 1. The tools: three plain functions.
# The docstrings matter: they become the tool descriptions the model reads.
# ---------------------------------------------------------------------------

def safe_path(path: str) -> Path:
    """Turn the model's path into a full one, and refuse anything outside FOLDER.
    This stops paths like "../other_project/a.py" or "C:/Windows/win.ini"."""
    full_path = (FOLDER / path).resolve()
    if not full_path.is_relative_to(FOLDER):
        raise ValueError(f"{path} is outside the folder {FOLDER}")
    return full_path


def read_file(path: str) -> str:
    """Return the full content of a text file.
    :param path: path to the file, e.g. "calc.py" or "src/main.py"
    """
    return safe_path(path).read_text(encoding="utf-8")


def list_files(path: str) -> str:
    """List the files and folders in a directory. Folder names end with "/".
    :param path: the directory to list; "." is the current folder
    """
    names = []
    for item in sorted(safe_path(path).iterdir()):
        if item.is_dir():
            names.append(item.name + "/")
        else:
            names.append(item.name)
    return "\n".join(names)


def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Replace old_text with new_text in a file (the first occurrence only).
    If old_text is empty, create the file (or overwrite it) with new_text.
    :param path: path to the file to change or create
    :param old_text: the exact text to find, copied from the file; "" to create a file
    :param new_text: the text to put in its place
    """
    file = safe_path(path)
    if old_text == "":
        file.write_text(new_text, encoding="utf-8")
        return f"Created {path}"
    content = file.read_text(encoding="utf-8")
    if old_text not in content:
        return f"Error: old_text was not found in {path}"
    file.write_text(content.replace(old_text, new_text, 1), encoding="utf-8")
    return f"Edited {path}"


TOOLS = {"read_file": read_file, "list_files": list_files, "edit_file": edit_file}


# ---------------------------------------------------------------------------
# Part 2. The prompt: the template from the top, filled in with the tool list.
# inspect reads each function's name, parameters and docstring, so the prompt
# always matches the code: add a function to TOOLS and the model knows about it.
# ---------------------------------------------------------------------------

def describe_tool(function) -> str:
    """For example: 'read_file(path: str) -> str' followed by its docstring."""
    return f"{function.__name__}{inspect.signature(function)}\n{inspect.getdoc(function)}"


TOOL_DESCRIPTIONS = "\n\n".join(describe_tool(f) for f in TOOLS.values())

SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.format(folder=FOLDER, tools=TOOL_DESCRIPTIONS)


# ---------------------------------------------------------------------------
# Part 3. The loop: ask the model, find a "tool: name({...})" line in its reply,
# run that tool, send the result back - and repeat until it simply answers.
# ---------------------------------------------------------------------------

def find_tool_call(reply: str):
    """Return (tool_name, arguments_as_json_text) if the reply asks for a tool, else None."""
    for line in reply.splitlines():
        line = line.strip()
        if line.startswith("tool:"):
            call = line[len("tool:"):].strip()      # 'read_file({"path": "calc.py"})'
            name, _, rest = call.partition("(")     # 'read_file', '{"path": "calc.py"})'
            return name.strip(), rest[:-1]          # drop the final ')'
    return None


def ask_claude(client, messages) -> str:
    """Send the whole conversation so far and return Claude's text reply."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=16_000,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    # The reply is a list of blocks; the model may think first, we keep only the text.
    return "".join(block.text for block in response.content if block.type == "text")


def main():
    client = anthropic.Anthropic()  # reads the ANTHROPIC_API_KEY environment variable
    messages = []                   # the conversation: the model remembers only this

    print("This is everything the model is told before your first question:\n")
    print(SYSTEM_PROMPT)
    print("\n" + "=" * 60)
    print("Mini Claude Code. Ask for something; an empty line quits.")
    while True:
        question = input("\nYou: ").strip()
        if not question:
            break
        messages.append({"role": "user", "content": question})

        # Keep asking the model until it answers without asking for a tool.
        while True:
            reply = ask_claude(client, messages)
            messages.append({"role": "assistant", "content": reply})
            print(f"\nClaude: {reply}")

            tool_call = find_tool_call(reply)
            if tool_call is None:
                break                                   # a normal answer: the user's turn

            name, arguments_json = tool_call
            try:
                arguments = json.loads(arguments_json)  # '{"path": "calc.py"}' -> a dict
                result = TOOLS[name](**arguments)       # run the Python function
            except Exception as error:                  # bad JSON, unknown tool, missing file...
                result = f"Error: {error}"              # tell the model, so it can try again
            print(f"  -> {result[:80]}")
            messages.append({"role": "user", "content": f"tool_result: {result}"})


if __name__ == "__main__":
    main()
