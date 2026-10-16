import sys
import json
import chromadb
from retriever.retriever import retrieve

RERANK = len(sys.argv) > 1 and sys.argv[1] == "rerank"
print("Reranker:", "ON" if RERANK else "OFF")

claims = json.load(open("data/eval_claims.json", encoding="utf-8"))

col = chromadb.PersistentClient(path="retriever/chroma_db").get_collection("wiki_evidence")
indexed = {m["source"] for m in col.get(include=["metadatas"])["metadatas"]}
claims = [c for c in claims if any(p in indexed for p in c["gold_pages"])]
print(f"Evaluating {len(claims)} claims")

KS = [1, 5, 10]
hits = {k: 0 for k in KS}
misses = []

for i, c in enumerate(claims):
    results = retrieve(c["claim"], k=max(KS), rerank=RERANK)
    sources = [e.source for e in results]
    gold = set(c["gold_pages"])
    found = False
    for k in KS:
        if gold & set(sources[:k]):
            hits[k] += 1
            found = True
    if not found:
        misses.append({"claim": c["claim"], "gold": c["gold_pages"], "got": sources[:3]})
    if i % 200 == 0:
        print(f"\r{i}/{len(claims)}", end="")

print()
for k in KS:
    print(f"recall@{k}: {hits[k] / len(claims):.3f}")

out = "data/recall_misses_rerank.json" if RERANK else "data/recall_misses.json"
json.dump(misses[:50], open(out, "w"), indent=1)
print(f"{len(misses)} claims missed at k=10 (first 50 saved to {out})")