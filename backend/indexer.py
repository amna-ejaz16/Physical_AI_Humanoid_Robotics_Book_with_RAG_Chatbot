"""
Optimized Indexer Script for RAG System
- Discovers .md/.mdx files
- Parses, cleans, chunks content
- Generates embeddings (supports batch if available)
- Uploads to Qdrant with metadata
"""


import argparse
import logging
from dotenv import load_dotenv
from config import load_config
from agent_client import GeminiClient
from rag_client import QdrantManager, TextChunker, MarkdownParser, discover_markdown_files

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main indexing function."""
    parser = argparse.ArgumentParser(description="Index book content into Qdrant")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force recreate collection (deletes existing data)"
    )
    args = parser.parse_args()

    # Load configuration
    load_dotenv()
    try:
        config = load_config()
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please ensure .env file exists with required variables:")
        logger.error("  - GEMINI_API_KEY")
        logger.error("  - QDRANT_URL")
        logger.error("  - QDRANT_API_KEY")
        return

    logger.info("=== Starting book content indexing ===")
    logger.info(f"Book content path: {config.rag.book_content_path}")
    logger.info(f"Chunk size: {config.rag.chunk_size} tokens")
    logger.info(f"Chunk overlap: {config.rag.chunk_overlap} tokens")

    # Initialize clients
    try:
        gemini_client = GeminiClient(config.agent)
        qdrant_manager = QdrantManager(config.qdrant)
        text_chunker = TextChunker(
            chunk_size=config.rag.chunk_size,
            chunk_overlap=config.rag.chunk_overlap
        )
    except Exception as e:
        logger.error(f"Failed to initialize clients: {e}")
        return

    # Create or force-recreate collection
    try:
        if args.force:
            try:
                qdrant_manager.client.delete_collection(config.qdrant.collection_name)
                logger.info(f"Deleted existing collection: {config.qdrant.collection_name}")
            except Exception as e:
                logger.warning(f"Collection deletion failed or did not exist: {e}")

        qdrant_manager.create_collection()
    except Exception as e:
        logger.error(f"Failed to create collection: {e}")
        return

    # Discover markdown/mdx files
    try:
        markdown_files = discover_markdown_files(config.rag.book_content_path)
        if not markdown_files:
            logger.warning(f"No markdown/mdx files found in {config.rag.book_content_path}")
            return
        logger.info(f"Found {len(markdown_files)} markdown/mdx files")
    except Exception as e:
        logger.error(f"Failed to discover markdown files: {e}")
        return

    # Process each file
    all_chunks = []
    all_embeddings = []
    failed_files = []

    for i, file_path in enumerate(markdown_files, 1):
        logger.info(f"Processing ({i}/{len(markdown_files)}): {file_path}")
        try:
            parsed = MarkdownParser.parse_markdown(file_path)

            if not parsed["content"].strip():
                logger.warning(f"  Skipping {file_path} - no content after cleaning")
                continue

            chunks = text_chunker.chunk_text(parsed["content"], file_path)
            logger.info(f"  Created {len(chunks)} chunks")

            # Generate embeddings for each chunk
            for j, chunk in enumerate(chunks):
                try:
                    embedding = gemini_client.generate_embedding(chunk["content"])
                    all_chunks.append(chunk)
                    all_embeddings.append(embedding)

                    if (j + 1) % 10 == 0:
                        logger.info(f"  Generated {j + 1}/{len(chunks)} embeddings")

                except Exception as e:
                    logger.error(f"  Failed to generate embedding for chunk {j} in file {file_path}: {e}")
                    continue

        except Exception as e:
            logger.error(f"  Failed to process {file_path}: {e}")
            failed_files.append(file_path)
            continue

    # Upload all chunks to Qdrant
    if all_chunks:
        logger.info(f"\n=== Uploading to Qdrant ===")
        logger.info(f"Total chunks to upload: {len(all_chunks)}")
        try:
            qdrant_manager.upload_chunks(all_chunks, all_embeddings)
            logger.info("✓ Successfully uploaded all chunks")
        except Exception as e:
            logger.error(f"Failed to upload chunks: {e}")
            return
    else:
        logger.warning("No chunks to upload")
        return

    # Summary
    logger.info("\n=== Indexing Complete ===")
    logger.info(f"Files processed: {len(markdown_files) - len(failed_files)}/{len(markdown_files)}")
    logger.info(f"Total chunks indexed: {len(all_chunks)}")

    if failed_files:
        logger.warning(f"\nFailed files ({len(failed_files)}):")
        for file in failed_files:
            logger.warning(f"  - {file}")

    # Test retrieval
    logger.info("\n=== Testing retrieval ===")
    try:
        test_query = "What is this book about?"
        test_embedding = gemini_client.generate_embedding(test_query, task_type="retrieval_query")
        results = qdrant_manager.search(test_embedding, top_k=3)
        logger.info(f"✓ Test retrieval successful - found {len(results)} chunks")
        for r in results:
            logger.info(f"Source: {r['source_file']}, Score: {r['score']}")
    except Exception as e:
        logger.error(f"Test retrieval failed: {e}")


if __name__ == "__main__":
    main()
