# ✨ MindMerge — Local RAG Academic AI Assistant

> **Turn your lecture PDFs into a private, intelligent AI tutor — fully offline.**

![License](https://img.shields.io/badge/license-MIT-green)
![Local AI](https://img.shields.io/badge/AI-100%25%20Local-blue)
![Powered by Ollama](https://img.shields.io/badge/Ollama-LLM-orange)
![RAG](https://img.shields.io/badge/Architecture-RAG-purple)

---

## 🚀 What is MindMerge?

**MindMerge** is a **privacy-first Academic AI Assistant** that converts your local lecture notes and PDFs into an **interactive knowledge base** using **Retrieval-Augmented Generation (RAG)**.

💡 Ask questions, get precise answers, and see **exact citations** — all **without sending your data to the cloud**.

---

## 🔐 Why MindMerge?

✔️ **100% Offline & Private** — Your data never leaves your machine  
✔️ **Zero Cost** — No API keys, no subscriptions  
✔️ **Source-Aware Answers** — Every response is backed by your PDFs  
✔️ **Fast & Lightweight** — Optimized local inference  
✔️ **Academic-Focused** — Built for students & researchers  

---

## 🌟 Key Features

🛡️ **Privacy by Design**  
All processing runs locally using **Ollama** — no cloud dependency.

📚 **Intelligent RAG Pipeline**  
Answers are grounded in your own lecture materials using semantic search.

⚡ **Zero-Cost AI**  
Powered by **TinyLlama** & **Nomic embeddings** — free forever.

📝 **Citation & References**  
Every answer includes exact PDF references.

🎨 **Modern Desktop UI**  
Clean, responsive dashboard built with **CustomTkinter**.

---

## 🏗️ Technology Stack

| Component        | Technology |
|-----------------|------------|
| 💬 LLM          | TinyLlama (Ollama) |
| 🧠 Embeddings   | nomic-embed-text |
| 📦 Vector Store | FAISS |
| 🔌 Backend      | Node.js, Express, LangChain |
| 🖥️ Frontend     | Python, CustomTkinter |

---

## 🛠️ Prerequisites

### 1️⃣ Install Ollama
Download from: https://ollama.com

Pull required models:
```bash
ollama pull nomic-embed-text
ollama pull tinyllama

⚙️ Installation
Backend (Node.js)
npm install --legacy-peer-deps

Frontend (Python)
pip install customtkinter requests

▶️ How to Run
Step 1: Start Backend
node server.mjs


✅ Expected:

🚀 TINYLLAMA Backend running on http://localhost:5000

Step 2: Launch GUI
python main.py

🧠 System Architecture (RAG Flow)
graph TD
    A[PDF Documents] --> B[Text Chunking]
    B --> C[Nomic Embeddings]
    C --> D[FAISS Vector Store]
    E[User Query] --> D
    D --> F[Context Retrieval]
    F --> G[Prompt Template]
    G --> H[TinyLlama (LLM)]
    H --> I[Answer + Citations]

Usage Guide
📁 Add Knowledge

Upload lecture PDFs using the sidebar button.

🧩 Indexing

Documents are split into 500-character chunks and embedded into FAISS.

💬 Ask Questions

Example:
Explain the matrix structure discussed in lecture 3
📍 Verify Sources

Check citation tags under each response to see exact references.

🧪 Troubleshooting
Issue	Solution
❌ Connection Error	Ensure backend is running on port 5000
⚠️ Ollama Offline	Confirm Ollama is running in system tray
📄 No References	Upload at least one PDF
🐢 Slow Indexing	Close heavy background applications

📄 License

MIT License — free to use, modify, and distribute.