import json
import re
from sentence_transformers import SentenceTransformer
import chromadb

WIKI_FILE = "data/wiki-pages/wiki-pages/wiki-001.jsonl"
MAX_PAGES = 3000       # sample size
CHUNK_WORDS = 200      # words per chunk

def clean_text(text):
    # FEVER tokenizes parentheses as -LRB- / -RRB-; restore them
    text = text.replace("-LRB-", "(").replace("-RRB-", ")")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text, chunk_words=CHUNK_WORDS):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_words):
        chunk = " ".join(words[i:i + chunk_words])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def load_pages(path, max_pages):
    pages = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if not entry.get("id") or not entry.get("text"):
                continue
            pages.append(entry)
            if len(pages) >= max_pages:
                break
    return pages

def main():
    print(f"Loading up to {MAX_PAGES} pages from {WIKI_FILE}...")
    pages = load_pages(WIKI_FILE, MAX_PAGES)
    print(f"Loaded {len(pages)} pages.")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="retriever/chroma_db")

    # Fresh collection each time we rebuild
    try:
        client.delete_collection("wiki_evidence")
    except Exception:
        pass
    collection = client.create_collection("wiki_evidence")

    ids, texts, embeddings, metadatas = [], [], [], []
    chunk_counter = 0

    for page in pages:
        clean = clean_text(page["text"])
        for chunk in chunk_text(clean):
            chunk_id = f"chunk_{chunk_counter}"
            ids.append(chunk_id)
            texts.append(chunk)
            metadatas.append({"source": page["id"]})
            chunk_counter += 1

    print(f"Embedding {len(texts)} chunks...")
    batch_size = 256
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size]
        batch_embeddings = model.encode(batch_texts).tolist()

        collection.add(
            ids=batch_ids,
            embeddings=batch_embeddings,
            documents=batch_texts,
            metadatas=batch_meta
        )
        print(f"\r{min(i + batch_size, len(texts))}/{len(texts)} chunks embedded", end="")

    print(f"\nDone. Indexed {chunk_counter} chunks from {len(pages)} pages into retriever/chroma_db")

if __name__ == "__main__":
    main()