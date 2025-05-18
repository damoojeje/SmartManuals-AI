# 🧠 SmartManuals-AI

**Local Semantic Q&A for Equipment Manuals and Part Catalogs**  
Built by [Damilare Eniolabi](mailto:damilareeniolabi@gmail.com) | GitHub: [@damoojeje](https://github.com/damoojeje)

---

SmartManuals-AI is a fully local RAG (Retrieval-Augmented Generation) pipeline that lets you ask intelligent questions from user manuals, service guides, parts catalogs, diagrams, and engineering drawings — **without any internet connection or cloud model**.

---

## ✅ Features

- 📚 Ingests and parses PDF manuals, images, and part tables
- 🧩 Converts data into searchable chunks and structured parts
- 🧠 Embeds using `sentence-transformers` into a local ChromaDB
- 💬 Answers natural questions using local Ollama models like `llama3`, `mistral`, or `gemma3`
- 🖥️ Simple Gradio dashboard for demo and interaction
- 🧠 Supports OCR, tables, and semantic search

---

## 🚀 Quickstart

### 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### ⚙️ Configure `.env`
Make sure `.env` is in your root folder and sets paths, model, and keyword options.

### 📁 Add PDFs
Drop your manuals into the `Manuals/` folder.

### 🏗️ Run the full pipeline
```bash
# Extract chunks, tables, images
python extract_text_and_tables.py

# Embed into Chroma
python embed_chunks_to_chroma.py

# Launch dashboard
python dashboard.py
```

> Or run everything with:
```bash
./run_all.sh      # macOS/Linux
run_all.bat       # Windows
```

---

## 🖥️ Project Structure
```
SmartManuals-AI/
├── Manuals/                # Your input folder
├── chroma_store/          # Local vector DB
├── images/                # OCR'd or extracted images
├── .env                   # All config values
├── chunks.jsonl           # Text + table chunks (auto)
├── tables.json            # Parsed tables (auto)
├── image_metadata.json    # OCR'd images (auto)
├── extract_text_and_tables.py
├── embed_chunks_to_chroma.py
├── query_ollama_rag.py
├── dashboard.py
├── run_all.bat / run_all.sh
├── requirements.txt
├── SETUP_GUIDE.md
└── README.md
```

---

## ❓ Example Queries

- "How do I access diagnostics on the Discover SE3 console?"
- "What does part A132-7 refer to?"
- "Where is the fuse on the Everest model?"
- "How do I immobilize the console for transport?"

---

## 🤖 Powered by
- 🧠 [Ollama](https://ollama.com/) – local LLM serving
- 🔍 [ChromaDB](https://www.trychroma.com/) – vector search
- 🧠 [Sentence Transformers](https://www.sbert.net/)
- 🖼️ [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- 🌐 [Gradio](https://gradio.app/) – web interface

---

## 📬 Contact
**Author**: [Damilare Eniolabi](mailto:damilareeniolabi@gmail.com)  
**GitHub**: [@damoojeje](https://github.com/damoojeje)

> Built for private, offline, and high-trust document intelligence.
