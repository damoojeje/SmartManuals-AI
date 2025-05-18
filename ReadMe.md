# 🛠️ ManualRAGProject Setup Guide

> Author: **Damilare Eniolabi**  
> GitHub: [@damoojeje](https://github.com/damoojeje)  
> Email: damilareeniolabi@gmail.com

---

## 📁 Folder Structure

```
ManualRAGProject/
├── Manuals/                  # Drop all your PDFs and Word docs here
├── images/                   # Auto-generated from OCR and image extraction
├── chroma_store/             # Chroma vector DB (auto-generated)
├── extract_text_and_tables.py
├── embed_chunks_to_chroma.py
├── query_ollama_rag.py
├── dashboard.py
├── run_all.bat / run_all.sh  # One-click runner (Windows / Linux)
├── .env                      # Environment variables config
├── requirements.txt
└── README.md / SETUP_GUIDE.md
```

---

## ✅ Installation

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

If you don’t have the file, install manually:
```bash
pip install sentence-transformers chromadb gradio requests pytesseract pymupdf python-dotenv
```

### 2. Install Tesseract OCR
- [Tesseract Download (Windows)](https://github.com/tesseract-ocr/tesseract/wiki)
- Add Tesseract to your system PATH

---

## 📥 Ingest Manuals

### 1. Drop files into `Manuals/`
Accepted file types:
- PDF (with text or scanned images)
- Word documents (optional future support)
- Diagrams and engineering drawings embedded in PDFs

---

## 🔎 Run the Pipeline

### 2. Extract chunks, tables, and images:
```bash
python extract_text_and_tables.py
```
Outputs:
- `chunks.jsonl`: page-level text chunks
- `tables.json`: structured part table entries
- `images/`: cropped diagrams
- `image_metadata.json`: OCR captions

### 3. Embed into Chroma:
```bash
python embed_chunks_to_chroma.py
```
Creates `chroma_store/` with all vectors stored and queryable.

---

## 🤖 Query Options

### CLI:
```bash
python query_ollama_rag.py
```
Enter a natural language question when prompted.

### Gradio UI:
```bash
python dashboard.py
```
Visit: http://localhost:7860 in your browser

### Or run full pipeline:
- **Windows**: `run_all.bat`
- **Linux/macOS**: `./run_all.sh`

---

## ⚙️ Using `.env` File

Modify the `.env` file to control your:
- Input/output paths
- Default model
- Reranking keywords
- Max chunk count

Example usage in Python:
```python
from dotenv import load_dotenv
import os
load_dotenv()
model = os.getenv("DEFAULT_MODEL")
keywords = os.getenv("RERANK_KEYWORDS").split(',')
```

---

## 🧠 Example Questions
- "How do I access diagnostics on a Discover SE3 console?"
- "What does part A132-7 refer to?"
- "Where is the fuse located on the Everest display?"
- "How do I immobilize the console for transport?"

---

## 🧩 Optional Enhancements
- Add `docx`, `xlsx`, `svg` parsing support
- Extract drawings and label callouts using bounding boxes
- Integrate with LangChain, LLaVA, or RAG-as-a-service

---

## 🤝 Credits
Powered locally by:
- [Ollama](https://ollama.com/) for model serving
- [Gradio](https://gradio.app/) for UI
- [Chroma](https://www.trychroma.com/) for vector search
- [Sentence-Transformers](https://www.sbert.net/) for embeddings
