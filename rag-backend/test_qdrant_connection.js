require('dotenv').config({ path: require('path').resolve(__dirname, '../.env') });
const { QdrantClient } = require('@qdrant/js-client-rest');

const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

console.log('QDRANT_URL:', QDRANT_URL);
console.log('Attempting connection to Qdrant...');

const qdrantClient = new QdrantClient({
    url: QDRANT_URL,
    apiKey: QDRANT_API_KEY,
});

async function testConnection() {
    try {
        console.log('Testing connection...');
        const collections = await qdrantClient.getCollections();
        console.log('Connected successfully!');
        console.log('Number of collections:', collections.collections.length);
        console.log('Collections:', collections.collections.map(c => c.name));

        const targetCollection = collections.collections.find(col => col.name === 'docusaurus_rag');
        if (targetCollection) {
            const collectionInfo = await qdrantClient.getCollection('docusaurus_rag');
            console.log(`\ndocusaurus_rag collection exists!`);
            console.log(`Points count: ${collectionInfo.points_count}`);
        } else {
            console.log('\ndocusaurus_rag collection does not exist yet.');
        }
    } catch (error) {
        console.error('Connection failed:', error.message);
        console.error('Error details:', error);
    }
}

testConnection();

// require('dotenv').config();
// const { QdrantClient } = require('@qdrant/js-client-rest');

// // Use the values from your .env file
// const QDRANT_URL = process.env.QDRANT_URL;
// const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

// console.log('QDRANT_URL:', QDRANT_URL);
// console.log('Attempting connection to Qdrant...');

// const qdrantClient = new QdrantClient({
//     url: QDRANT_URL,  // Note: using 'url' instead of 'host' for cloud instances
//     apiKey: QDRANT_API_KEY,
// });

// async function testConnection() {
//     try {
//         console.log('Testing connection...');
//         const collections = await qdrantClient.getCollections();
//         console.log('Connected successfully!');
//         console.log('Number of collections:', collections.collections.length);
//         console.log('Collections:', collections.collections.map(c => c.name));

//         // Check specifically for the docusaurus_rag collection
//         const targetCollection = collections.collections.find(col => col.name === 'docusaurus_rag');
//         if (targetCollection) {
//             const collectionInfo = await qdrantClient.getCollection('docusaurus_rag');
//             console.log(`\ndocusaurus_rag collection exists!`);
//             console.log(`Points count: ${collectionInfo.points_count}`);
//         } else {
//             console.log('\ndocusaurus_rag collection does not exist yet.');
//         }
//     } catch (error) {
//         console.error('Connection failed:', error.message);
//         console.error('Error details:', error);
//     }
// }

// testConnection();