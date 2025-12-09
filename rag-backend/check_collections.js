require('dotenv').config({ path: require('path').resolve(__dirname, '../.env') });
const { QdrantClient } = require('@qdrant/js-client-rest');

const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

const qdrantClient = new QdrantClient({
    url: process.env.QDRANT_URL,
    apiKey: process.env.QDRANT_API_KEY,
    checkCompatibility: false
});

async function checkCollections() {
    try {
        console.log('Connecting to Qdrant...');
        const collections = await qdrantClient.getCollections();

        console.log('Available collections:');
        for (const collection of collections.collections) {
            console.log(`- Collection: ${collection.name}`);

            // Get collection info to see number of vectors
            const collectionInfo = await qdrantClient.getCollection(collection.name);
            console.log(`  Points count: ${collectionInfo.points_count}`);
            console.log(`  Vector size: ${collectionInfo.config.params.vectors.size}`);
            console.log(`  Distance: ${collectionInfo.config.params.vectors.distance}`);
            console.log('');
        }
    } catch (error) {
        console.error('Error connecting to Qdrant:', error.message);
    }
}

checkCollections();