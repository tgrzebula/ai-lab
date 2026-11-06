# RAG indexing, inside out

How LlamaIndex turns text into a searchable index, one step at a time. No LLM, no API
key: only the retrieval half of RAG, with a local embedding model
(`paraphrase-multilingual-MiniLM-L12-v2`, downloaded on first run, ~470 MB).

`inspect_index.py` loads three short texts from `data/`, splits them into 9 chunks,
embeds each chunk into one 384-number vector, saves the index to `storage/` and ranks
every chunk against a few questions, next to the words each question shares with it.

`inspect_index_minimal.py` is the same idea in 20 lines: three sentences, three vectors,
one question. Start there.

```bash
pip install -r requirements.txt
python inspect_index_minimal.py
python inspect_index.py
python inspect_index.py "your own question"
```

## What it shows

- The unit is a chunk, not a word: 9 chunks give 9 vectors, whether a chunk has 12 words or 48.
- The search compares vectors, not words. *"my script stopped with an error message"* shares no
  word with any chunk and still lands on the traceback paragraph.
- The retriever's score is plain cosine similarity: computed by hand with numpy, it
  matches LlamaIndex to the third decimal.
- What gets embedded is not just the chunk: LlamaIndex prepends metadata
  (`file_path: ...`). Embedding `node.text` alone gave different scores (0.516 vs 0.465).
- A small model has limits. The Polish *"Jak naprawić przebitą dętkę?"* finds the
  bicycle text but ranks the chain chunk above the puncture one. *"Java"* puts the coffee
  island first and Python's "Unlike Java" second: one word carries little meaning.
