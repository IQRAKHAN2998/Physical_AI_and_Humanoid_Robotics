#!/usr/bin/env python3
"""
Test the full backend workflow by running the document embedding process
"""
import asyncio
import sys
from pathlib import Path

# Add the rag-backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

async def test_full_workflow():
    print("Testing full backend workflow...")

    try:
        # Import the embed_documents function
        from api import embed_documents
        print("✅ Successfully imported embed_documents function")

        # Run the embedding process
        print("\n🚀 Starting full document embedding process...")
        await embed_documents()
        print("✅ Full document embedding process completed successfully!")

        return True
    except Exception as e:
        print(f"❌ Error in full workflow: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_full_workflow())

    if success:
        print("\n🎉 Full backend workflow test passed!")
    else:
        print("\n⚠️  Full backend workflow test failed!")
        sys.exit(1)