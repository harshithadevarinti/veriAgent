import json, glob, random, re
from sentence_transformers import SentenceTransformer
import chromadb

DEV_FILE = "data/shared_task_dev.jsonl"
WIKI_GLOB = "data/wiki-pages/wiki-pages/wiki-*.jsonl"
N_CLAIMS = 2000          # dev claims to evaluate on
N_DISTRACTORS = 5000     # random extra pages
CHUNK_WORDS = 200
random.seed(0)

def clean(t):
    t = t.replace("-LRB-", "(").replace("-RRB-", ")")
    return re.sub(r"\s+", " ", t).strip()

def chunks(t):
    w = t.split()
    return [" ".join(w[i:i + CHUNK_WORDS]) for i in range(0, len(w), CHUNK_WORDS)]

# 1. Pick dev claims that have gold evidence
claims, gold_pages = [], set()
with open(DEV_FILE, encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        if d["label"] == "NOT ENOUGH INFO":
            continue
        pages = {e[2] for group in d["evidence"] for e in group if e[2]}
        if not pages:
            continue
        claims.append({"claim": d["claim"], "label": d["label"], "gold_pages": sorted(pages)})
        gold_pages |= pages
        if len(claims) >= N_CLAIMS:
            break
json.dump(claims, open("data/eval_claims.json", "w"), indent=1)
print(f"{len(claims)} claims, {len(gold_pages)} gold pages")

# 2. Scan the dump: keep gold pages + reservoir of distractors
keep, distractors = {}, []
seen = 0
for path in sorted(glob.glob(WIKI_GLOB)):
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            if not d["id"] or not d["text"]:
                continue
            if d["id"] in gold_pages:
                keep[d["id"]] = d["text"]
            else:
                seen += 1
                if len(distractors) < N_DISTRACTORS:
                    distractors.append(d)
                else:
                    j = random.randint(0, seen - 1)
                    if j < N_DISTRACTORS:
                        distractors[j] = d
    print(f"scanned {path}", end="\r")
for d in distractors:
    keep[d["id"]] = d["text"]
print(f"\nIndexing {len(keep)} pages ({len(gold_pages & set(keep))} gold found)")

# 3. Embed and store
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="retriever/chroma_db")
try:
    client.delete_collection("wiki_evidence")
except Exception:
    pass
col = client.create_collection("wiki_evidence")

ids, texts, metas = [], [], []
for title, text in keep.items():
    for c in chunks(clean(text)):
        ids.append(f"chunk_{len(ids)}")
        texts.append(c)
        metas.append({"source": title})

B = 256
for i in range(0, len(texts), B):
    col.add(ids=ids[i:i+B], documents=texts[i:i+B], metadatas=metas[i:i+B],
            embeddings=model.encode(texts[i:i+B]).tolist())
    print(f"\r{min(i+B, len(texts))}/{len(texts)} chunks", end="")
print("\nDone.")