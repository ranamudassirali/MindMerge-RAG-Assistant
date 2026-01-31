✨ MindMerge RAG Assistant

MindMerge is a privacy-first Academic AI Assistant that transforms your local lecture notes into an interactive knowledge base. By leveraging Retrieval-Augmented Generation (RAG), it allows you to chat with your PDFs using a local LLM (TinyLlama) without any data leaving your hardware.

🌟 Key Features

🛡️ 100% Private: All processing happens on your local CPU/GPU. No cloud, no leaks.

📚 Intelligent RAG: Searches your PDFs to provide answers based on your actual study materials.

⚡ Zero-Cost: No subscription or API keys required (powered by Ollama).

📝 Citation Support: Every answer includes references to the specific PDFs used.

🎨 Modern UI: High-performance dashboard built with CustomTkinter.

🏗️ Technology Stack

Component

Technology

Language Model

TinyLlama (via Ollama)

Embeddings

Nomic-Embed-Text (via Ollama)

Vector DB

FAISS (Facebook AI Similarity Search)

Backend

Node.js + Express + LangChain

Frontend

Python + CustomTkinter

🛠️ Prerequisites & Setup

1. Install Ollama

Download and install Ollama. Once installed, pull the required models:

# High-quality local embeddings
ollama pull nomic-embed-text

# Lightweight, fast chat model
ollama pull tinyllama


2. Backend Installation (Node.js)

In the project root, install the dependencies. We use --legacy-peer-deps to ensure compatibility with LangChain's community packages.

npm install --legacy-peer-deps


3. Frontend Installation (Python)

Install the GUI requirements:

pip install customtkinter requests


🚦 Execution Guide

Step 1: Fire up the Backend

node server.mjs


Expected output: 🚀 TINYLLAMA Backend running on http://localhost:5000

Step 2: Launch the GUI

python main.py


📖 Usage Workflow

Add Knowledge: Click the 📁 Add Lecture PDF button in the sidebar.

Indexing: The system chunks the text into 500-character segments and creates a mathematical "map" (Embeddings).

Query: Type a question like "Explain the matrix structure mentioned in the lecture notes."

Reference: Review the 📍 Reference tags at the bottom of the AI response to see which document provided the data.

🧠 System Architecture

graph TD
    A[PDF Document] -->|Loader| B(Text Splitting)
    B -->|Nomic Embeddings| C[FAISS Vector Store]
    D[User Query] -->|Similarity Search| C
    C -->|Top Context Chunks| E[Prompt Template]
    D --> E
    E -->|Context + Query| F[TinyLlama Model]
    F -->|Response| G[GUI Output]


❓ Troubleshooting

Issue

Solution

"Connection Error"

Ensure the Node.js server is running and port 5000 is open.

"Ollama might be offline"

Check if the Ollama application is active in your system tray.

Empty References

Make sure you have uploaded at least one PDF before asking study-specific questions.

Slow Indexing

Close heavy background apps; indexing utilizes CPU for generating embeddings.

📄 License

This project is open-source under the MIT License.

Developed for Academic Excellence — Keep Learning! 🚀