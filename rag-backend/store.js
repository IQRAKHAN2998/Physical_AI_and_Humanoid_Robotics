
require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });
const { QdrantClient } = require('@qdrant/js-client-rest');

const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;
const COLLECTION_NAME = 'docusaurus_rag';

const qdrantClient = new QdrantClient({
    url: QDRANT_URL,  // Cloud instance URL
    apiKey: QDRANT_API_KEY,
});

async function createCollection() {
    const collections = await qdrantClient.getCollections();
    const collectionExists = collections.collections.some(col => col.name === COLLECTION_NAME);

    if (!collectionExists) {
        await qdrantClient.createCollection(COLLECTION_NAME, {
            vectors: { size: 768, distance: 'Cosine' }, // Adjust size based on your embedding model output
        });
        console.log(`Collection '${COLLECTION_NAME}' created.`);
    } else {
        console.log(`Collection '${COLLECTION_NAME}' already exists.`);
    }
}

async function storeEmbeddings(embeddings) {
    await createCollection();

    const points = embeddings.map((data, index) => ({
        id: index,
        vector: data.embedding,
        payload: { text: data.text, source: data.source },
    }));

    // Qdrant allows batch upsert for performance
    const BATCH_SIZE = 100;
    for (let i = 0; i < points.length; i += BATCH_SIZE) {
        const batch = points.slice(i, i + BATCH_SIZE);
        await qdrantClient.upsert(COLLECTION_NAME, {
            wait: true,
            batch: {
                ids: batch.map(p => p.id),
                vectors: batch.map(p => p.vector),
                payloads: batch.map(p => p.payload),
            },
        });
    }

    console.log(`Stored ${embeddings.length} embeddings in collection '${COLLECTION_NAME}'.`);
}

async function searchEmbeddings(queryEmbedding, limit = 3) {
    const searchResult = await qdrantClient.search(COLLECTION_NAME, {
        vector: queryEmbedding,
        limit: limit,
        append_payload: true,
    });
    return searchResult.map(result => result.payload);
}

module.exports = { storeEmbeddings, searchEmbeddings };
