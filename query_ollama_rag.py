# ✅ query_ollama_rag.py
# Retrieves top semantic matches from Chroma and queries local Ollama model for response

import chromadb
from sentence_transformers import SentenceTransformer, util
import requests
import json
import os
from dotenv import load_dotenv

# ---------------------------
# 🔐 Load Config from .env
# ---------------------------
load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_store")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "manual_chunks")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("DEFAULT_MODEL", "llama3")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
MAX_CHUNKS = int(os.getenv("MAX_CONTEXT_CHUNKS", 5))

# ---------------------------
# 🔌 Load DB + Embedder
# ---------------------------
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(COLLECTION_NAME)
embedder = SentenceTransformer(EMBED_MODEL)

# ---------------------------
# 🔎 Semantic Search + Rerank
# ---------------------------
def retrieve_chunks(question, top_k=MAX_CHUNKS):
    results = collection.query(
        query_texts=[question],
        n_results=top_k * 3
    )

    question_vec = embedder.encode(question, convert_to_tensor=True)
    scored = []
    for i, text in enumerate(results["documents"][0]):
        emb = embedder.encode(text, convert_to_tensor=True)
        score = float(util.cos_sim(question_vec, emb))
        scored.append({
            "text": text,
            "score": score,
            "metadata": results["metadatas"][0][i]
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

# ---------------------------
# 🤖 Ask Ollama
# ---------------------------
def ask_ollama(prompt, model=OLLAMA_MODEL):
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"model": model, "prompt": prompt, "stream": False})
    )
    if response.status_code != 200:
        raise RuntimeError(response.text)
    return response.json()["response"].strip()

# ---------------------------
# 🎯 Run RAG Q&A
# ---------------------------
def run_query(question):
    top_chunks = retrieve_chunks(question)
    context = "\n\n".join([c["text"] for c in top_chunks])
    prompt = f"""
You are a technical assistant trained to answer questions using manuals and parts catalogs.
Use only the context below to answer the question.
If the answer is not in the context, say "I don't know."

<context>
{context}
</context>

Question: {question}
Answer:"""

    answer = ask_ollama(prompt)
    print("\n✅ Answer:")
    print(answer)

# ---------------------------
# 🧪 Test
# ---------------------------
if __name__ == "__main__":
    q = input("🔎 Ask a question: ")
    run_query(q)
