

require('dotenv').config({ path: require('path').resolve(__dirname, '../.env') });
const { processDocs } = require('./embed');
const { storeEmbeddings } = require('./store');

async function runEmbeddingProcess() {
    try {
        console.log('Starting embedding process...');

        // Process the documentation files to generate embeddings
        const embeddings = await processDocs();
        console.log(`Generated ${embeddings.length} embeddings`);

        // Store the embeddings in Qdrant
        await storeEmbeddings(embeddings);
        console.log('Embeddings stored successfully!');
    } catch (error) {
        console.error('Error during embedding process:', error);
    }
}

runEmbeddingProcess();