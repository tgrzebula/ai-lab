"""The same three-sentence index as inspect_index_minimal.py, asked in a loop.

The model loads and the sentences are embedded once; each question only embeds itself.
"""

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

texts = [
    "To repair a puncture, take out the inner tube and glue a patch on it.",
    "Espresso is made by pressing hot water through finely ground coffee.",
    "When a Python program crashes, read the traceback from the bottom up.",
]
index = VectorStoreIndex([Document(text=t) for t in texts])
retriever = index.as_retriever(similarity_top_k=3)

print(f"Indexed {len(texts)} sentences. Ask in any language, empty line to quit.")
while question := input("\nQuestion: ").strip():
    for hit in retriever.retrieve(question):
        print(f"{hit.score:.3f}  {hit.node.text}")
