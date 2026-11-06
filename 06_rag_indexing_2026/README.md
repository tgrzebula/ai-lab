# RAG indexing, inside out

The smallest possible look at what a LlamaIndex vector index stores. No LLM, no API key:
only the retrieval half of RAG, with a local embedding model
(`paraphrase-multilingual-MiniLM-L12-v2`, downloaded on first run, ~470 MB).

| Script | What it is |
|--------|------------|
| `inspect_index_minimal.py` | Indexes three sentences, prints the vector stored for each, ranks them against one fixed question. Start here |
| `inspect_index.py` | The same index, asked in a loop: the model and sentences load once, each question embeds only itself |

```bash
pip install -r requirements.txt
python inspect_index_minimal.py
python inspect_index.py         # type questions, empty line to quit
```

## Result

Output of `inspect_index_minimal.py`:

```
704e9a12  384 numbers  [0.017, -0.012, -0.04] ...
6031d179  384 numbers  [-0.09, -0.011, -0.035] ...
9daeb272  384 numbers  [-0.024, -0.046, 0.018] ...

Question: my code stopped with an error
0.402  When a Python program crashes, read the traceback from the bottom up.
0.011  Espresso is made by pressing hot water through finely ground coffee.
-0.136  Dogs need a long walk every day.
```

Node ids are random and change every run; the vectors and scores stay the same.

## What it shows

- The unit is a chunk, not a word: 3 sentences give 3 vectors of 384 numbers each.
- The search compares vectors, not words. *"my code stopped with an error"* shares no
  word with the Python sentence and still ranks it first (0.402 vs 0.011 and -0.136).

