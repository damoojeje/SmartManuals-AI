# ✅ dashboard.py
# Gradio-powered UI for asking questions to your local manual RAG system

import gradio as gr
from query_ollama_rag import retrieve_chunks, ask_ollama
from dotenv import load_dotenv
import os

# ---------------------------
# 🔐 Load Config from .env
# ---------------------------
load_dotenv()
OLLAMA_MODEL = os.getenv("DEFAULT_MODEL", "llama3")
MAX_CHUNKS = int(os.getenv("MAX_CONTEXT_CHUNKS", 5))

# ---------------------------
# 🧠 Format prompt for Ollama
# ---------------------------
def build_prompt(question, top_chunks):
    context = "\n\n".join([c["text"] for c in top_chunks])
    return f"""
You are a technical assistant trained to answer questions using manuals and parts catalogs.
Use only the context below to answer the question.
If the answer is not in the context, say "I don't know."

<context>
{context}
</context>

Question: {question}
Answer:"""

# ---------------------------
# 🎯 Full Query Handler
# ---------------------------
def run_rag_interface(user_question, model_name):
    chunks = retrieve_chunks(user_question, top_k=MAX_CHUNKS)
    if not chunks:
        return "No relevant information found."
    prompt = build_prompt(user_question, chunks)
    try:
        answer = ask_ollama(prompt, model=model_name)
        return answer
    except Exception as e:
        return f"❌ Ollama error: {e}"

# ---------------------------
# 🎛️ UI
# ---------------------------
with gr.Blocks() as demo:
    gr.Markdown("""# 🧠 Ask Your Manuals
Ask any technical or parts question from your embedded manuals. Uses local Ollama models.
""")
    with gr.Row():
        question = gr.Textbox(label="Your Question", placeholder="e.g. What does part A132-7 refer to?")
        model = gr.Dropdown(choices=["llama3", "mistral", "gemma3"], value=OLLAMA_MODEL, label="Model")
    ask_btn = gr.Button("🔍 Ask")
    output = gr.Textbox(label="Answer", lines=6)

    ask_btn.click(fn=run_rag_interface, inputs=[question, model], outputs=[output])

# ---------------------------
# 🚀 Launch
# ---------------------------
if __name__ == "__main__":
    demo.launch()
