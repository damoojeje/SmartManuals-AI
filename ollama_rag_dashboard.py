# ✅ Gradio Dashboard: RAG over Manuals with Ollama
# Local interface to query your own manuals and get answers via llama3/mistral/gemma3

import gradio as gr
import requests
import json
from sentence_transformers import SentenceTransformer, util
import chromadb

# ---------------------------
# ⚙️ Configuration
# ---------------------------
OLLAMA_HOST = "http://localhost:11434"
CHROMA_PATH = "./chroma_store"
COLLECTION_NAME = "manual_chunks"
MAX_CONTEXT_CHUNKS = 4
DEFAULT_MODEL = "llama3"

# ---------------------------
# 🔌 Load RAG Components
# ---------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

# ---------------------------
# 🔍 Query Function
# ---------------------------
def query_manuals(question, model_filter=None, doc_type_filter=None, top_k=5, rerank_keywords=None):
    where_filter = {"model": model_filter.lower()} if model_filter else None

    results = collection.query(
        query_texts=[question],
        n_results=top_k * 5,
        where=where_filter
    )
    if not results["documents"] or not results["documents"][0]:
        return []

    question_embedding = embedder.encode(question, convert_to_tensor=True)
    reranked = []
    for i, text in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        embedding = embedder.encode(text, convert_to_tensor=True)
        sim_score = float(util.cos_sim(question_embedding, embedding))
        keyword_score = sum(1 for kw in rerank_keywords or [] if kw.lower() in text.lower())
        final_score = 0.8 * sim_score + 0.2 * keyword_score
        reranked.append({"score": final_score, "text": text, "metadata": meta})

    reranked.sort(key=lambda x: x["score"], reverse=True)
    return reranked[:top_k]

# ---------------------------
# 💬 Ask Ollama
# ---------------------------
def ask_ollama(prompt, model=DEFAULT_MODEL):
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"model": model, "prompt": prompt, "stream": False})
    )
    if response.status_code != 200:
        raise RuntimeError(f"Ollama error: {response.status_code} {response.text}")
    return response.json()["response"].strip()

# ---------------------------
# 🎯 Full RAG Pipeline
# ---------------------------
def run_rag_qa(user_question, model_choice):
    results = query_manuals(
        question=user_question,
        model_filter=None,
        doc_type_filter=None,
        top_k=MAX_CONTEXT_CHUNKS,
        rerank_keywords=["diagnostic", "immobilize", "system", "screen", "service"]
    )
    if not results:
        return "No relevant documents found."

    context = "\n\n".join([r["text"].strip() for r in results])
    prompt = f"""
You are a technical assistant trained to answer questions using equipment manuals.
Use only the provided context to answer the question.
If the answer is not clearly in the context, reply: 'I don't know.'

Context:
{context}

Question: {user_question}
Answer:"""

    try:
        return ask_ollama(prompt, model_choice)
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---------------------------
# 🖥️ Gradio Interface
# ---------------------------
with gr.Blocks() as demo:
    gr.Markdown("""# 🧠 Manual QA via Ollama
Ask a technical question and get local answers using your own PDF manual database.
""")
    with gr.Row():
        question = gr.Textbox(label="Your Question", placeholder="e.g. How do I access diagnostics on the SE3 console?")
        model_choice = gr.Dropdown(choices=["llama3", "mistral", "gemma3"], value="llama3", label="Ollama Model")
    submit = gr.Button("🔍 Ask")
    answer = gr.Textbox(label="Answer", lines=6)

    submit.click(fn=run_rag_qa, inputs=[question, model_choice], outputs=[answer])

# ---------------------------
# 🚀 Launch App
# ---------------------------
demo.launch()
