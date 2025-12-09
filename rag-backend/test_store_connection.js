require('dotenv').config({ path: require('path').resolve(__dirname, '../.env') });
const { QdrantClient } = require('@qdrant/js-client-rest');

const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

console.log('QDRANT_URL from rag-backend:', QDRANT_URL);

const qdrantClient = new QdrantClient({
    url: QDRANT_URL,
    apiKey: QDRANT_API_KEY,
});

async function testStoreConnection() {
    try {
        console.log('Testing connection from rag-backend...');
        const collections = await qdrantClient.getCollections();
        console.log('Connected successfully from rag-backend!');
        console.log('Number of collections:', collections.collections.length);
    } catch (error) {
        console.error('Connection failed from rag-backend:', error.message);
        console.error('Full error:', error);
    }
}

testStoreConnection();