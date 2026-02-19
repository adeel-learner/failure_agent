from pathlib import Path
import json
import faiss
import numpy as np

from langchain_community.embeddings import HuggingFaceEmbeddings

from memory.database import get_connection

# -------------------------
# Vector Store Setup
# -------------------------

INDEX_PATH = Path(__file__).parent / "failures.index"

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load or create FAISS index
if INDEX_PATH.exists():
    index = faiss.read_index(str(INDEX_PATH))
    metadata_store_path = INDEX_PATH.with_suffix(".meta.json")
    with open(metadata_store_path, "r") as f:
        metadata_store = json.load(f)
else:
    index = faiss.IndexFlatL2(384)  # embedding dimension for all-MiniLM-L6-v2
    metadata_store = {}  # maps idx -> event_id

# Helper to save index
def save_index():
    faiss.write_index(index, str(INDEX_PATH))
    metadata_store_path = INDEX_PATH.with_suffix(".meta.json")
    with open(metadata_store_path, "w") as f:
        json.dump(metadata_store, f)


# -------------------------
# Store Failure Embedding
# -------------------------

def store_failure_embedding(event_id: int, record: dict):
    """
    Create embedding for failure record and store in FAISS
    """

    text = record.get("event_description", "") + " " + " ".join(record.get("root_causes", []))
    vector = embedding_model.embed_documents([text])[0]
    vector = np.array(vector, dtype="float32").reshape(1, -1)

    index.add(vector)
    metadata_store[str(len(metadata_store))] = event_id

    save_index()


# -------------------------
# Search Similar Failures
# -------------------------

def search_similar_failures(root_causes: list, top_k: int = 5):
    """
    Given root causes, return top_k similar failures
    """
    if not root_causes or index.ntotal == 0:
        return []

    query_text = " ".join(root_causes)
    query_vector = embedding_model.embed_documents([query_text])[0]
    query_vector = np.array(query_vector, dtype="float32").reshape(1, -1)

    distances, indices = index.search(query_vector, top_k)

    results = []
    conn = get_connection()
    cursor = conn.cursor()

    for idx, dist in zip(indices[0], distances[0]):
        if idx == -1:
            continue
        event_id = metadata_store.get(str(idx))
        if not event_id:
            continue
        cursor.execute("SELECT * FROM failures WHERE id=?", (event_id,))
        row = cursor.fetchone()
        if row:
            results.append({
                "event_description": row["event_description"],
                "root_causes": json.loads(row["root_causes"]),
                "pattern_summary": row["pattern_summary"],
                "distance": float(dist)
            })
    conn.close()
    return results
