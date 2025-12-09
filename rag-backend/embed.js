
require('dotenv').config({ path: require('path').resolve(__dirname, '../.env') });
const fs = require('fs');
const path = require('path');
const { QdrantClient } = require('@qdrant/js-client-rest');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Configuration
const COLLECTION_NAME = 'docusaurus-rag';
const VECTOR_SIZE = 768;
const DISTANCE = 'Cosine';
const DOCS_PATH = 'D:/4_quarter4_AIDD/Physical_AI_and_Humanoid_Robotics/docs';
const SUPPORTED_EXTENSIONS = ['.md', '.txt', '.pdf', '.html'];

// Initialize clients
let qdrantClient;
if (process.env.QDRANT_URL && process.env.QDRANT_API_KEY) {
  // Use cloud Qdrant instance
  qdrantClient = new QdrantClient({
    url: process.env.QDRANT_URL,
    apiKey: process.env.QDRANT_API_KEY,
    checkCompatibility: false
  });
  console.log("Using Qdrant Cloud instance");
} else {
  // Fallback to local Qdrant instance
  qdrantClient = new QdrantClient({
    url: 'http://localhost:6333',
    checkCompatibility: false
  });
  console.log("Using local Qdrant instance");
}

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || process.env.GEMINI_KEY);
const model = genAI.getGenerativeModel({ model: 'text-embedding-004' });

/**
 * Converts various file formats to plain text
 */
async function convertToText(filePath) {
  const ext = path.extname(filePath).toLowerCase();

  if (ext === '.txt') {
    return fs.readFileSync(filePath, 'utf8');
  } else if (ext === '.md') {
    const markdown = fs.readFileSync(filePath, 'utf8');
    // Simple markdown to text conversion (remove basic markdown syntax)
    return markdown
      .replace(/#{1,6}\s*/g, '') // Remove headers
      .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold
      .replace(/\*(.*?)\*/g, '$1') // Remove italic
      .replace(/\[(.*?)\]\(.*?\)/g, '$1') // Remove links
      .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
      .replace(/`{1,3}[^`]*`{1,3}/g, '') // Remove code blocks
      .replace(/^\s*[-*+]\s+/gm, '') // Remove list markers
      .replace(/^\s*\d+\.\s+/gm, '') // Remove numbered list markers
      .trim();
  } else if (ext === '.html') {
    const html = fs.readFileSync(filePath, 'utf8');
    // Simple HTML to text conversion (basic tag removal)
    return html
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove script tags
      .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '') // Remove style tags
      .replace(/<[^>]+>/g, ' ') // Remove all other tags
      .replace(/&nbsp;/g, ' ') // Replace non-breaking spaces
      .replace(/&amp;/g, '&') // Replace ampersands
      .replace(/&lt;/g, '<') // Replace less than
      .replace(/&gt;/g, '>') // Replace greater than
      .replace(/\s+/g, ' ') // Normalize whitespace
      .trim();
  } else if (ext === '.pdf') {
    // For PDF, we need to install pdf-parse: npm install pdf-parse
    const pdfParse = require('pdf-parse');
    const pdfBuffer = fs.readFileSync(filePath);
    const pdfData = await pdfParse(pdfBuffer);
    return pdfData.text;
  } else {
    throw new Error(`Unsupported file extension: ${ext}`);
  }
}

/**
 * Splits text into chunks of 500-800 words
 */
function splitIntoChunks(text, minWords = 500, maxWords = 800) {
  const words = text.split(/\s+/);
  const chunks = [];
  let startIndex = 0;

  while (startIndex < words.length) {
    let endIndex = Math.min(startIndex + maxWords, words.length);

    // If we're near the end, make sure we don't go over maxWords
    if (endIndex - startIndex <= maxWords && endIndex === words.length) {
      chunks.push(words.slice(startIndex, endIndex).join(' '));
      break;
    }

    // If the chunk is too small, extend it
    if (endIndex - startIndex < minWords) {
      endIndex = Math.min(startIndex + minWords, words.length);
    }

    chunks.push(words.slice(startIndex, endIndex).join(' '));
    startIndex = endIndex;
  }

  return chunks;
}

/**
 * Generates embeddings using Gemini API
 */
// async function generateEmbedding(text) {
//   try {
//     const result = await model.embedContent(text);
//     return result.embedding.values; // Assuming this returns the vector array
//   } catch (error) {
//     console.error('Error generating embedding:', error);
//     throw error;
//   }
// }

async function generateEmbedding(text) {
  try {
    const result = await model.embedContent(text);
    console.log("Embedding length:", result.embedding.values.length); // 🔹 ye line add hui
    return result.embedding.values;
  } catch (error) {
    console.error('Error generating embedding:', error);
    throw error;
  }
}

/**
 * Checks if collection exists and creates it if it doesn't
 */
async function ensureCollectionExists() {
  try {
    await qdrantClient.getCollection(COLLECTION_NAME);
    console.log(`✅ Collection '${COLLECTION_NAME}' already exists`);
  } catch (error) {
    if (error.status === 404) {
      console.log(`📦 Creating collection '${COLLECTION_NAME}'...`);
      await qdrantClient.createCollection(COLLECTION_NAME, {
        vectors: {
          size: VECTOR_SIZE,
          distance: DISTANCE,
        },
      });
      console.log(`✅ Collection '${COLLECTION_NAME}' created successfully`);
    } else {
      throw error;
    }
  }
}

/**
 * Reads all files from the docs directory with supported extensions
 */
function getAllFiles(dirPath, arrayOfFiles = []) {
  const files = fs.readdirSync(dirPath);

  files.forEach((file) => {
    const filePath = path.join(dirPath, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      getAllFiles(filePath, arrayOfFiles);
    } else {
      const ext = path.extname(file).toLowerCase();
      if (SUPPORTED_EXTENSIONS.includes(ext)) {
        arrayOfFiles.push(filePath);
      }
    }
  });

  return arrayOfFiles;
}

/**
 * Main embedding function
 */
async function embedDocuments() {
  try {
    console.log('🚀 Starting document embedding process...');

    // Ensure collection exists
    await ensureCollectionExists();

    // Get all files to process
    const files = getAllFiles(DOCS_PATH);
    console.log(`📁 Found ${files.length} files to process`);

    if (files.length === 0) {
      console.log('⚠️ No supported files found in the docs directory');
      return;
    }

    let totalPointsInserted = 0;

    for (const file of files) {
      console.log(`\n📄 Processing file: ${file}`);

      try {
        // Convert file to text
        const text = await convertToText(file);

        if (!text.trim()) {
          console.log(`⚠️ Skipping empty file: ${file}`);
          continue;
        }

        // Split into chunks
        const chunks = splitIntoChunks(text);
        console.log(`✂️  Split into ${chunks.length} chunks`);

        // Process each chunk
        for (let i = 0; i < chunks.length; i++) {
          const chunk = chunks[i];

          if (!chunk.trim()) {
            continue; // Skip empty chunks
          }

          // Generate embedding
          const vector = await generateEmbedding(chunk);

          // Prepare point for insertion with numeric ID
          const point = {
            id: parseInt(`${Date.now()}${i.toString().padStart(3, '0')}`.slice(-16)), // Numeric ID based on timestamp
            vector: Array.from(vector), // Ensure vector is a proper array
            payload: {
              text: chunk.substring(0, 10000), // Limit text length to avoid payload size issues
              source: file,
              chunk_index: i,
            },
          };

          // Upsert the point with proper error handling
          try {
            await qdrantClient.upsert(COLLECTION_NAME, {
              points: [point],
              wait: true,  // Wait for operation to complete
            });
            console.log(`💾 Chunk ${i + 1}/${chunks.length} inserted`);
            totalPointsInserted++;
          } catch (upsertError) {
            console.error(`❌ Error inserting chunk ${i + 1} from ${file}:`, upsertError.message);
            // Print more detailed error info for debugging
            console.error(`   Error details:`, upsertError);
            // Continue to next chunk instead of stopping the entire process
            continue;
          }
        }

        console.log(`✅ Completed processing: ${file}`);
      } catch (error) {
        console.error(`❌ Error processing file ${file}:`, error.message);
        continue; // Continue with next file
      }
    }

    console.log(`\n📈 Summary: ${totalPointsInserted} points inserted into collection '${COLLECTION_NAME}'`);
    console.log('✅ Embedding Finished');
  } catch (error) {
    console.error('❌ Fatal error during embedding process:', error);
    process.exit(1);
  }
}

// Run the embedding process
if (require.main === module) {
  if (!process.env.GEMINI_API_KEY && !process.env.GEMINI_KEY) {
    console.error('❌ Error: GEMINI_API_KEY or GEMINI_KEY environment variable is required');
    console.error('Please set your Gemini API key: export GEMINI_API_KEY=your_api_key');
    process.exit(1);
  }

  embedDocuments();
}

module.exports = {
  convertToText,
  splitIntoChunks,
  generateEmbedding,
  ensureCollectionExists,
  getAllFiles,
  embedDocuments,
};



