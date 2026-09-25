# agents/controller.py
from .llm import ask
from .verifier import verify
from .schemas import Verdict, Evidence

MAX_ITERS = 3

def rewrite_query(claim: str, previous_queries: list[str]) -> str:
    return ask(
        "Write ONE new search query to find evidence that could verify or refute the claim. "
        "It must differ from previous queries. Output only the query.",
        f"CLAIM: {claim}\nPREVIOUS QUERIES: {previous_queries}",
        max_tokens=60,
    ).strip()

def confidence(v: dict, evidence: list[Evidence]) -> float:
    ret = sum(e.score for e in evidence) / len(evidence) if evidence else 0.0
    conf = 0.65 * v["confidence"] + 0.35 * min(ret, 1.0)
    if v.get("conflict"):
        conf *= 0.7
    return round(conf, 3)

def check_claim(claim: str, retrieve) -> Verdict:
    """`retrieve(query, k)` is Member 1's function -> list[Evidence]."""
    queries, all_evidence = [claim], []
    for i in range(1, MAX_ITERS + 1):
        new = retrieve(queries[-1], k=5)
        seen = {e.text for e in all_evidence}
        all_evidence += [e for e in new if e.text not in seen]

        v = verify(claim, all_evidence)
        done = v["label"] != "NOT_ENOUGH_INFO" and not v.get("conflict")
        if done or i == MAX_ITERS:
            return Verdict(claim=claim, label=v["label"], confidence=confidence(v, all_evidence),
                           rationale=v["rationale"], evidence=all_evidence, iterations=i)
        queries.append(rewrite_query(claim, queries))