# agents/verifier.py
from .llm import ask_json
from .schemas import Evidence

SYSTEM = """You are a strict fact-checker. Given a CLAIM and numbered EVIDENCE passages,
decide using ONLY the evidence (not your own knowledge):
- SUPPORTED: evidence clearly entails the claim.
- REFUTED: evidence clearly contradicts the claim.
- NOT_ENOUGH_INFO: evidence is missing, unrelated, or ambiguous.
Output: {"label": "...", "confidence": 0.0-1.0, "rationale": "1-2 sentences",
 "used_evidence": [indices], "conflict": true/false}
Set conflict=true if some passages support and others contradict."""

def verify(claim: str, evidence: list[Evidence]) -> dict:
    ev_text = "\n".join(f"[{i}] ({e.source}) {e.text}" for i, e in enumerate(evidence))
    return ask_json(SYSTEM, f"CLAIM: {claim}\n\nEVIDENCE:\n{ev_text or '(none)'}")