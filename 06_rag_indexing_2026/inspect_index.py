"""Build a LlamaIndex vector index step by step and print what each step produces.

No LLM and no API key: only the retrieval half of RAG, with a local embedding model.

    python inspect_index.py                       # built-in example questions
    python inspect_index.py "your own question"
"""

import re
import sys
from pathlib import Path

import numpy as np
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import MetadataMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

HERE = Path(__file__).parent
# Multilingual, so a question in Polish can find an English chunk. 384 numbers per vector.
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
QUESTIONS = [
    "How do I fix a flat tyre?",
    "Jak naprawić przebitą dętkę?",  # Polish: no word in common with the text
    "my script stopped with an error message",
    "Java",  # one word, two meanings in the data
]

Settings.llm = None  # retrieval only; stops LlamaIndex from reaching for OpenAI
embed_model = HuggingFaceEmbedding(model_name=MODEL)
Settings.embed_model = embed_model


def header(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def words(text):
    return set(re.findall(r"\w+", text.lower())) - {"a", "an", "the", "i", "do", "my", "how", "to", "with"}


# 1. Load: one Document per file, the whole text plus metadata.
header("1. LOAD - one Document per file")
documents = SimpleDirectoryReader(HERE / "data").load_data()
for doc in documents:
    print(f"{doc.metadata['file_name']:<12} {len(doc.text):>4} characters")

# 2. Split: Documents are cut into chunks (Nodes). This is the unit that gets a vector.
header("2. SPLIT - documents become chunks (Nodes)")
splitter = SentenceSplitter(chunk_size=80, chunk_overlap=10)
nodes = splitter.get_nodes_from_documents(documents)
for i, node in enumerate(nodes):
    preview = node.text.replace("\n", " ")[:60]
    print(f"[{i:>2}] {node.metadata['file_name']:<12} {preview}...")
print(f"\n{len(documents)} documents -> {len(nodes)} chunks (chunk_size=80 tokens, overlap=10)")

# 3. Embed: each chunk becomes ONE vector, however many words it has.
header("3. EMBED - one vector per chunk, not per word")
# What gets embedded is not node.text alone: LlamaIndex prepends metadata (here file_path).
embedded = [n.get_content(metadata_mode=MetadataMode.EMBED) for n in nodes]
print(f"text actually embedded for chunk 0:\n{embedded[0]!r}\n")
vectors = np.array(embed_model.get_text_embedding_batch(embedded))
for i, node in enumerate(nodes):
    print(f"[{i:>2}] {len(node.text.split()):>3} words -> [{', '.join(f'{x:+.3f}' for x in vectors[i][:5])}, ...]")
position = {n.node_id: i for i, n in enumerate(nodes)}
print(f"\nvector matrix:{vectors.shape[0]} chunks x {vectors.shape[1]} numbers")

# 4. Index: VectorStoreIndex is these vectors plus the chunk texts, nothing more.
header("4. INDEX - persisted to ./storage")
index = VectorStoreIndex(nodes)  # embeds again internally; step 3 was just to show it
storage = HERE / "storage"
index.storage_context.persist(persist_dir=storage)
for f in sorted(storage.iterdir()):
    print(f"{f.name:<28} {f.stat().st_size:>8} bytes")
print("default__vector_store.json = node id -> vector;  docstore.json = node id -> text")

# 5. Retrieve: the question is embedded the same way and compared to every chunk vector.
questions = sys.argv[1:] or QUESTIONS
retriever = index.as_retriever(similarity_top_k=3)
for question in questions:
    header(f"5. RETRIEVE - {question!r}")
    q = np.array(embed_model.get_query_embedding(question))
    cosine = vectors @ q / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(q))
    print("cosine  shared words  chunk")
    for i in np.argsort(-cosine):
        shared = words(question) & words(nodes[i].text)
        preview = nodes[i].text.replace("\n", " ")[:42]
        print(f"{cosine[i]:+.3f}  {', '.join(sorted(shared)) or '-':<12}  [{i:>2}] {preview}")
    top = retriever.retrieve(question)
    print("\nLlamaIndex retriever top 3:", ", ".join(f"[{position[r.node.node_id]}] {r.score:.3f}" for r in top))

# Reload from disk: no re-embedding of documents, only of the question.
header("6. RELOAD - the index from disk, without touching data/")
reloaded = load_index_from_storage(StorageContext.from_defaults(persist_dir=storage))
hit = reloaded.as_retriever(similarity_top_k=1).retrieve(questions[0])[0]
print(f"{hit.score:.3f}  {hit.node.text[:70]!r}")
