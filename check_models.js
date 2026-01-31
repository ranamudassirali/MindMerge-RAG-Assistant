import { config } from "dotenv";
config();
import { GoogleGenerativeAI } from "@google/generative-ai";

async function listModels() {
  try {
    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
    // This internal method fetches the exact list for your key
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${process.env.GOOGLE_API_KEY}`);
    const data = await response.json();
    
    console.log("=== Available Models for your Key ===");
    data.models.forEach(m => {
      console.log(`- Model Name: ${m.name}`);
      console.log(`  Methods: ${m.supportedGenerationMethods.join(", ")}\n`);
    });
  } catch (error) {
    console.error("Error listing models:", error);
  }
}

listModels();