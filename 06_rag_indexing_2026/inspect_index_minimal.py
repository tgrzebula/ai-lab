"""The smallest possible vector index: three sentences, one question."""

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Each Document is short enough to stay one chunk, so: 3 texts -> 3 vectors.
texts = [
    "To repair a puncture, take out the inner tube and glue a patch on it.",
    "Espresso is made by pressing hot water through finely ground coffee.",
    "When a Python program crashes, read the traceback from the bottom up.",
]
index = VectorStoreIndex([Document(text=t) for t in texts])

for node_id, vector in index.vector_store.data.embedding_dict.items():
    print(f"{node_id[:8]}  {len(vector)} numbers  {[round(x, 3) for x in vector[:3]]} ...")

question = "my code stopped with an error"
print(f"\nQuestion: {question}")
for hit in index.as_retriever(similarity_top_k=3).retrieve(question):
    print(f"{hit.score:.3f}  {hit.node.text}")
