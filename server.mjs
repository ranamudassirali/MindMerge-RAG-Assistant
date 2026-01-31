import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import multer from "multer";
import fs from "fs";
import path from "path";
import { config } from "dotenv";

import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";
import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OllamaEmbeddings, ChatOllama } from "@langchain/ollama";

config();

const app = express();
const PORT = 5000;
const DOCUMENTS_DIR = "./documents";
const FAISS_INDEX_PATH = "./faiss_index";

// Ensure required directories exist
if (!fs.existsSync(DOCUMENTS_DIR)) fs.mkdirSync(DOCUMENTS_DIR);

app.use(cors());
app.use(bodyParser.json());

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, DOCUMENTS_DIR),
  filename: (req, file, cb) => cb(null, file.originalname),
});
const upload = multer({ storage });

// Initialize local embeddings (Nomic is highly recommended for Ollama setups)
const embeddings = new OllamaEmbeddings({
  model: "nomic-embed-text",
  baseUrl: "http://localhost:11434",
});

let vectorStore = null;

/**
 * Loads existing FAISS index into memory on startup.
 */
const loadExistingIndex = async () => {
  if (fs.existsSync(FAISS_INDEX_PATH)) {
    try {
      vectorStore = await FaissStore.load(FAISS_INDEX_PATH, embeddings);
      console.log("✅ Local Knowledge Base loaded (TinyLlama mode).");
    } catch (err) {
      console.error("⚠️ Note: Knowledge base not found or Ollama is offline.");
    }
  }
};
loadExistingIndex();

/**
 * CHAT ENDPOINT
 * Optimized for local TinyLlama processing.
 */
app.post("/chat", async (req, res) => {
  try {
    const { message } = req.body;
    if (!message) return res.json({ reply: "Hello! I am TinyLlama. How can I help with your studies?", sources: [] });

    let contextText = "No local documents found.";
    let sources = [];

    // Attempt retrieval from FAISS if vectorStore is initialized
    if (vectorStore) {
      try {
        const retriever = vectorStore.asRetriever({ k: 2 }); // Keep k low for smaller models
        const docs = await retriever.invoke(message);
        if (docs.length > 0) {
          contextText = docs.map((d) => d.pageContent).join("\n\n");
          sources = [...new Set(docs.map((d) => path.basename(d.metadata.source)))];
        }
      } catch (e) {
        console.warn("⚠️ Retrieval issue:", e.message);
      }
    }

    // Initialize Local Chat Model (TinyLlama)
    const model = new ChatOllama({
      model: "tinyllama", 
      baseUrl: "http://localhost:11434",
      temperature: 0.1, // Low temperature for higher accuracy in academic answers
    });

    // Short, focused prompt suitable for a 1.1B parameter model
    const prompt = `Context: ${contextText}\n\nQuestion: ${message}\n\nAssistant Answer:`;

    console.log("🤖 TinyLlama is processing...");
    const response = await model.invoke(prompt);

    res.json({ 
      reply: response.content, 
      sources: sources 
    });

  } catch (err) {
    console.error("❌ LOCAL AI ERROR:", err.message);
    res.status(500).json({ error: "Ollama communication error. Ensure 'tinyllama' is running." });
  }
});

/**
 * UPLOAD ENDPOINT
 * Handles PDF ingestion and local indexing.
 */
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).send("No file uploaded.");
    
    console.log(`📄 Processing and indexing: ${req.file.originalname}`);
    
    /**
     * Updated PDFLoader with splitPages: false.
     * This often bypasses detailed font-parsing issues (TT warnings) 
     * by treating the document as a single stream before splitting manually.
     */
    const loader = new PDFLoader(req.file.path, {
      splitPages: false,
    });
    
    const loadedDocs = await loader.load();
    
    // Chunking optimized for local retrieval
    const splitter = new RecursiveCharacterTextSplitter({ chunkSize: 500, chunkOverlap: 100 });
    const splits = await splitter.splitDocuments(loadedDocs);

    if (!vectorStore) {
      vectorStore = await FaissStore.fromDocuments(splits, embeddings);
    } else {
      await vectorStore.addDocuments(splits);
    }

    // Save the index locally to avoid re-indexing everything later
    await vectorStore.save(FAISS_INDEX_PATH);
    res.json({ message: "File successfully indexed locally!" });
  } catch (err) {
    console.error("❌ Indexing Failed:", err.message);
    res.status(500).send("Error indexing file.");
  }
});

app.listen(PORT, () => console.log(`🚀 TINYLLAMA Backend running on http://localhost:${PORT}`));