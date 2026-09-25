from sentence_transformers import SentenceTransformer
import chromadb
from agents.schemas import Evidence

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="retriever/chroma_db")
collection = client.get_collection("wiki_evidence")

def retrieve(query: str, k: int = 2) -> list[Evidence]:
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=k)

    evidence_list = []
    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        similarity = 1 / (1 + distance)
        evidence_list.append(Evidence(
            text=results["documents"][0][i],
            source=results["metadatas"][0][i]["source"],
            score=similarity
        ))
    return evidence_list

if __name__ == "__main__":
    result = retrieve("Who won the 1986 NBA Finals?", k=3)
    for e in result:
        print(e)
        print("---")