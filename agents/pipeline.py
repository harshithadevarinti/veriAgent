# agents/pipeline.py
import json
from .decomposer import decompose
from .controller import check_claim

def verify_response(response: str, retrieve) -> list:
    verdicts = [check_claim(c, retrieve) for c in decompose(response)]
    with open("trace.jsonl", "a") as f:
        f.write(json.dumps([v.model_dump() for v in verdicts]) + "\n")
    return verdicts