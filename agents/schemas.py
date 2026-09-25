from typing import List, Literal, Optional
from pydantic import BaseModel

class Evidence(BaseModel):
    text: str
    source: str
    score: float = 0.0          # retrieval/rerank score, roughly 0-1

class Verdict(BaseModel):
    claim: str
    label: Literal["SUPPORTED", "REFUTED", "NOT_ENOUGH_INFO"]
    confidence: float           # 0-1
    rationale: str
    evidence: List[Evidence] = []
    iterations: int = 1