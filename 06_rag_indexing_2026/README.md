# RAG indexing, inside out

The smallest possible look at what a LlamaIndex vector index stores. No LLM, no API key:
only the retrieval half of RAG, with a local embedding model
(`paraphrase-multilingual-MiniLM-L12-v2`, downloaded on first run, ~470 MB).

`inspect_index.py` indexes three sentences, prints the vector stored for each, then
ranks them against one question.

```bash
pip install -r requirements.txt
python inspect_index.py
```

## What it shows

- The unit is a chunk, not a word: 3 sentences give 3 vectors of 384 numbers each.
- The search compares vectors, not words. *"my code stopped with an error"* shares no
  word with the Python sentence and still ranks it first (0.402 vs 0.078 and 0.011).
