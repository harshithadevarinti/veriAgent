import math
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
from agents.schemas import Evidence

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="retriever/chroma_db")
collection = client.get_collection("wiki_evidence")
_reranker = None

def _get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _reranker

def retrieve(query: str, k: int = 2, rerank: bool = False, candidates: int = 30) -> list[Evidence]:
    n = max(candidates, k) if rerank else k
    q = model.encode(query).tolist()
    res = collection.query(query_embeddings=[q], n_results=n)

    ev = []
    for i in range(len(res["ids"][0])):
        ev.append(Evidence(
            text=res["documents"][0][i],
            source=res["metadatas"][0][i]["source"],
            score=1 / (1 + res["distances"][0][i]),
        ))

    if rerank:
        raw = _get_reranker().predict([(query, e.text) for e in ev])
        ev = [Evidence(text=e.text, source=e.source, score=1 / (1 + math.exp(-float(s))))
              for e, s in zip(ev, raw)]
        ev.sort(key=lambda e: e.score, reverse=True)

    return ev[:k]

if __name__ == "__main__":
    for e in retrieve("Who won the 1986 NBA Finals?", k=3, rerank=True):
        print(e.source, round(e.score, 3))