"""Ingestion script for Markdown files in `backend/knowledge/`.

Reads all `.md` files, parses chunks separated by `##` headings,
extracts HTML comment metadata (`<!-- category: ..., escalate: true ... -->`),
generates Gemini vector embeddings, and seeds/upserts into Supabase pgvector `documentation` table.
"""

import os
import re
import glob
import logging
from typing import List, Dict, Any
from src.rag.retriever import generate_embedding
from src.db.supabase_client import get_supabase_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge")


def parse_metadata_comment(comment_str: str) -> Dict[str, Any]:
    """Parses key-value pairs inside HTML comments like:
    `<!-- category: shipping, escalate: true, keywords: delivery -->`
    """
    metadata: Dict[str, Any] = {}
    if not comment_str:
        return metadata

    # Extract key: value pairs separated by commas
    pairs = comment_str.split(",")
    for pair in pairs:
        if ":" in pair:
            key, val = pair.split(":", 1)
            key = key.strip().lower()
            val = val.strip()

            # Parse booleans & strings
            if val.lower() == "true":
                metadata[key] = True
            elif val.lower() == "false":
                metadata[key] = False
            else:
                metadata[key] = val
    return metadata


def parse_markdown_file(file_path: str) -> List[Dict[str, Any]]:
    """Splits markdown file by `##` headings into chunks with content and metadata."""
    chunks = []
    file_basename = os.path.basename(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split by heading ##
    raw_sections = re.split(r"(^|\n)##\s+", text)

    for sec in raw_sections:
        sec = sec.strip()
        if not sec:
            continue

        lines = sec.split("\n")
        heading = lines[0].strip()
        body_lines = lines[1:]

        metadata: Dict[str, Any] = {"file": file_basename, "heading": heading}
        content_lines = []

        for line in body_lines:
            # Check for HTML comment line: <!-- ... -->
            comment_match = re.search(r"<!--\s*(.*?)\s*-->", line)
            if comment_match:
                extracted_meta = parse_metadata_comment(comment_match.group(1))
                metadata.update(extracted_meta)
            else:
                content_lines.append(line)

        body_content = "\n".join(content_lines).strip()
        if body_content:
            full_chunk_text = f"## {heading}\n{body_content}"
            chunks.append({
                "content": full_chunk_text,
                "metadata": metadata
            })

    return chunks


def ingest_all_knowledge_files():
    """Main execution loop to ingest all markdown files in backend/knowledge/."""
    logger.info(f"📂 Scanning Knowledge Base directory: {KNOWLEDGE_DIR}")
    md_files = glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md"))

    if not md_files:
        logger.warning(f"⚠️ No markdown files found in {KNOWLEDGE_DIR}. Add files like 'shipping_delivery.md'.")
        return

    supabase = get_supabase_client()
    total_ingested = 0

    for file_path in md_files:
        logger.info(f"📄 Processing file: {os.path.basename(file_path)}...")
        chunks = parse_markdown_file(file_path)

        for chunk in chunks:
            content = chunk["content"]
            metadata = chunk["metadata"]

            logger.info(f"🔍 Generating embedding for chunk heading: '{metadata.get('heading', 'Untitled')}'")
            embedding = generate_embedding(content)

            try:
                # Format vector array as string for pgvector insertion
                row = {
                    "content": content,
                    "metadata": metadata,
                    "embedding": f"[{','.join(map(str, embedding))}]"
                }
                supabase.table("documentation").insert(row).execute()
                total_ingested += 1
                logger.info(f"✅ Ingested chunk: '{metadata.get('heading')}'")
            except Exception as e:
                logger.error(f"❌ Error inserting chunk into database: {e}")

    logger.info(f"🎉 Ingestion Complete! Successfully stored {total_ingested} chunk(s) in Supabase.")


if __name__ == "__main__":
    ingest_all_knowledge_files()
