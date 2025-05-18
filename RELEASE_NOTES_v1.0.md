# 🚀 SmartManuals-AI v1.0 Release Notes

**Release Date:** May 18, 2025  
**Author:** [Damilare Eniolabi](mailto:damilareeniolabi@gmail.com) ([@damoojeje](https://github.com/damoojeje))

---

## 🎉 What's Included in v1.0

SmartManuals-AI is a local-first semantic document QA system built for PDF manuals, part catalogs, and technical drawings. Version 1.0 includes a fully working pipeline from ingestion to interactive querying.

### ✅ Core Features
- ⚙️ **Full RAG stack**: PDF/diagram ingestion → embedding → local LLM QA
- 🧠 **Text + Table + OCR extraction** using PyMuPDF + Tesseract
- 💾 **Embedding + indexing** via SentenceTransformers and Chroma
- 🤖 **Local model querying** using [Ollama](https://ollama.com/) (LLaMA 3, Mistral, Gemma)
- 🌐 **Interactive Gradio dashboard** with model selection and top-k tuning

---

## 📁 Project Structure
- `extract_text_and_tables.py` – PDF to structured chunks and image OCR
- `embed_chunks_to_chroma.py` – Embeds JSONL chunks to ChromaDB
- `query_ollama_rag.py` – CLI script for querying with local LLM
- `dashboard.py` – Simple web UI for testing RAG loop
- `run_all.bat` / `run_all.sh` – One-click full pipeline launcher
- `.env` – Fully configurable paths and model settings

---

## 📚 Docs & Dev Assets
- `README.md` – Full GitHub landing overview
- `SETUP_GUIDE.md` – Local install + execution
- `TODO.md` – Future roadmap
- `CONTRIBUTING.md` – Dev & PR guidelines
- `LICENSE` – MIT Open License

---

## 🚀 Ready To:
- Embed thousands of equipment manuals
- Power factory or field-side offline agents
- Extend into OCR-heavy diagrams, vision-language models
- Integrate with internal document platforms (e.g. wiki.js)

---

## 🙌 Shoutout
Thank you to the open-source foundations: Sentence Transformers, ChromaDB, Gradio, PyMuPDF, Tesseract OCR, and Ollama.

---

> Built with care and clarity by **Damilare Eniolabi** – [@damoojeje](https://github.com/damoojeje)  
> For questions, feedback, or integrations: [damilareeniolabi@gmail.com](mailto:damilareeniolabi@gmail.com)
