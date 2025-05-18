#!/bin/bash

# ✅ run_all.sh
# One-command runner for full RAG setup (Linux/macOS)
# Extract, embed, and launch Gradio UI for local Ollama-powered manual QA

echo "[1/3] Extracting text, tables, and images..."
python3 extract_text_and_tables.py

echo "[2/3] Embedding chunks and table rows into vector store..."
python3 embed_chunks_to_chroma.py

echo "[3/3] Launching Gradio dashboard on http://localhost:7860 ..."
python3 dashboard.py


# Run using the following command
#chmod +x run_all.sh
#./run_all.sh
