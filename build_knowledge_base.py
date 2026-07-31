import os
import shutil
import hashlib
import chromadb
from sentence_transformers import SentenceTransformer
from scraper import crawl_website

DATABASE_FOLDER = "chroma_db"
COLLECTION_NAME = "ait_website_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150

def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            last_space = text.rfind(" ", start, end)
            if last_space > start + 300:
                end = last_space

        chunk = text[start:end].strip()

        if len(chunk) >= 100:
            chunks.append(chunk)

        if end >= text_length:
            break

        # Ensure forward progress to avoid infinite loops
        next_start = end - overlap
        start = max(start + 1, next_start)

    return chunks

def create_chunk_id(url, chunk_number):
    value = f"{url}_{chunk_number}"
    return hashlib.md5(value.encode("utf-8")).hexdigest()

def clear_existing_db(folder_path):
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Cleared previous database at '{folder_path}'")
        except PermissionError:
            print(f"Warning: Could not delete '{folder_path}'. Ensure open handles are closed.")

def build_database():
    print("\nStarting AIT website data collection...\n")
    pages = crawl_website(max_pages=80)

    if not pages:
        print("No website pages were collected. Exiting database build.")
        return

    clear_existing_db(DATABASE_FOLDER)

    client = chromadb.PersistentClient(path=DATABASE_FOLDER)
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Atria Institute of Technology website data"}
    )

    print("\nLoading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    documents = []
    metadatas = []
    ids = []

    for page in pages:
        chunks = split_text(page["text"])
        for number, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "url": page["url"],
                "title": page["title"] or "AIT Website",
                "chunk_number": number,
            })
            ids.append(create_chunk_id(page["url"], number))

    if not documents:
        print("No text chunks extracted from collected pages.")
        return

    print(f"\nCreating embeddings and storing {len(documents)} chunks...")

    batch_size = 32
    for start in range(0, len(documents), batch_size):
        end = min(start + batch_size, len(documents))

        batch_documents = documents[start:end]
        embeddings = model.encode(
            batch_documents,
            normalize_embeddings=True,
            show_progress_bar=False
        ).tolist()

        collection.add(
            ids=ids[start:end],
            documents=batch_documents,
            metadatas=metadatas[start:end],
            embeddings=embeddings
        )

        print(f"Stored {end}/{len(documents)} chunks")

    print("\nKnowledge base created successfully!")
    print(f"Pages collected: {len(pages)}")
    print(f"Text chunks stored: {len(documents)}")

if __name__ == "__main__":
    build_database()