# ✅ embed_chunks_to_chroma.py
# Embeds text and table chunks into Chroma DB with metadata for RAG

import os
import json
from sentence_transformers import SentenceTransformer
import chromadb
from tqdm import tqdm

# ---------------------------
# ⚙️ Configuration
# ---------------------------
JSONL_TEXT_CHUNKS = "chunks.jsonl"
JSON_TABLES = "tables.json"
CHROMA_PATH = "./chroma_store"
COLLECTION_NAME = "manual_chunks"
BATCH_SIZE = 16

# ---------------------------
# 🔌 Load Chroma + Embedder
# ---------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

if COLLECTION_NAME in [c.name for c in client.list_collections()]:
    collection = client.get_collection(COLLECTION_NAME)
else:
    collection = client.create_collection(COLLECTION_NAME)

# ---------------------------
# 📄 Load chunks
# ---------------------------
all_records = []

# Text chunks
with open(JSONL_TEXT_CHUNKS, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        all_records.append({
            "id": item["chunk_id"],
            "text": item["text"],
            "metadata": {
                "source_file": item["source_file"],
                "type": "text",
                "page": item.get("page", -1)
            }
        })

# Table rows
with open(JSON_TABLES, "r", encoding="utf-8") as f:
    tables = json.load(f)
    for table in tables:
        for i, row in enumerate(table["rows"]):
            text = f"Part #{row['part_number']} ({row['qty']}x): {row['description']}"
            chunk_id = f"{table['source_file']}::table_{table['page']}_row_{i+1}"
            all_records.append({
                "id": chunk_id,
                "text": text,
                "metadata": {
                    "source_file": table["source_file"],
                    "type": "table_row",
                    "page": table["page"]
                }
            })

# ---------------------------
# 🧠 Embed + Store
# ---------------------------
print(f"🔍 Embedding {len(all_records)} records...")

for i in tqdm(range(0, len(all_records), BATCH_SIZE)):
    batch = all_records[i:i + BATCH_SIZE]
    texts = [r["text"] for r in batch]
    ids = [r["id"] for r in batch]
    metadatas = [r["metadata"] for r in batch]
    embeddings = embedder.encode(texts).tolist()

    collection.add(
        documents=texts,
        ids=ids,
        metadatas=metadatas,
        embeddings=embeddings
    )

print("✅ All chunks embedded and stored in Chroma.")
