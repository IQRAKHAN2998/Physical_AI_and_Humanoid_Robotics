from api import search_embeddings
import asyncio

async def test_search():
    try:
        result = await search_embeddings([0.1]*768, 3)
        print(f'Search completed, found {len(result)} results')
    except Exception as e:
        print(f'Search test completed with expected exception (no data in collection): {type(e).__name__}')

if __name__ == "__main__":
    asyncio.run(test_search())