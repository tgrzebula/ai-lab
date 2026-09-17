# 01 — GPT Hello World (2024)

My first calls to the OpenAI API, November 2024. Kept as written.

| Script | Model |
|--------|-------|
| `hello_world.py` — the first call I ever made | `gpt-3.5-turbo` |
| `haiku_4o.py` — haiku about recursion, in Polish | `gpt-4o` |
| `haiku_4omini.py` — same prompt, cheaper model | `gpt-4o-mini` |
| `create_vector_embeddings.py` — text to embedding vector | `text-embedding-3-large` |
| `generate_an_image.py` — two images from a prompt | `dall-e-2` |

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."    # PowerShell: $env:OPENAI_API_KEY = "sk-..."
python hello_world.py
```
