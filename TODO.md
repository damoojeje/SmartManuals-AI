# ✅ TODO – SmartManuals-AI Roadmap

This file outlines planned improvements and optional enhancements for future development.

---

## 📌 Immediate Priorities

- [ ] ✅ Add `.env` references to all scripts (✅ done in core modules)
- [ ] 🔄 Auto-rebuild ChromaDB when new manuals are added
- [ ] 📁 Detect and ingest `.docx` and `.xlsx` files
- [ ] 🧠 Enhance table understanding with better row parsing
- [ ] 📷 Add LLaVA or similar image-grounded reasoning

---

## 🧪 Testing & Evaluation

- [ ] 🔍 Build a set of unit test prompts for accuracy validation
- [ ] 🧠 Compare local RAG to GPT-4 baseline (manuals vs. OpenAI)
- [ ] ⏱️ Benchmark embedding + search latency

---

## 🌍 Dashboard Enhancements

- [ ] ✅ Add model selector (✅ done)
- [ ] 📄 Show top chunks used in final prompt
- [ ] 📋 Toggle between table/text/image results
- [ ] 💬 Add session chat history with context

---

## 🧑‍💻 Developer Features

- [ ] 🔐 Protect `.env` and add `.env.example`
- [ ] 🛠️ Create a Dockerfile for local deployment
- [ ] ⚙️ Add Makefile / CLI wrapper for scripted execution
- [ ] 🧪 Add tests for chunking + metadata extraction

---

## 🧩 Optional Integrations

- [ ] 📸 Use OCR + image captioning on full diagrams
- [ ] 🧠 Add LangChain agent support
- [ ] 🧠 Integrate Hugging Face Spaces demo version
- [ ] 🤝 Connect to wiki.js or internal doc server

---

*Built by [@damoojeje](https://github.com/damoojeje)*
