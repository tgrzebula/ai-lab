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

## Result

```
1c22683c  384 numbers  [-0.062, -0.038, 0.107] ...
82b3eacf  384 numbers  [-0.09, -0.011, -0.035] ...
da51bcbd  384 numbers  [-0.024, -0.046, 0.018] ...

Question: my code stopped with an error
0.402  When a Python program crashes, read the traceback from the bottom up.
0.078  To repair a puncture, take out the inner tube and glue a patch on it.
0.011  Espresso is made by pressing hot water through finely ground coffee.
```

Node ids are random and change every run; the vectors and scores stay the same.

## What it shows

- The unit is a chunk, not a word: 3 sentences give 3 vectors of 384 numbers each.
- The search compares vectors, not words. *"my code stopped with an error"* shares no
  word with the Python sentence and still ranks it first (0.402 vs 0.078 and 0.011).
