@echo off

:: ✅ run_all.bat
:: One-click runner for full RAG pipeline (Windows)
:: Extract, embed, and launch Gradio UI for local Ollama-powered Q&A

:: Step 1: Extract data from manuals
echo [1/3] Extracting text, tables, and images...
python extract_text_and_tables.py

:: Step 2: Embed to Chroma
echo [2/3] Embedding chunks and table rows into vector store...
python embed_chunks_to_chroma.py

:: Step 3: Launch dashboard
echo [3/3] Launching web dashboard at http://localhost:7860 ...
python dashboard.py

pause
