# agents/pipeline.py
from .decomposer import decompose
from .controller import check_claim

def verify_response(response: str, retrieve) -> list:
    return [check_claim(c, retrieve) for c in decompose(response)]

import json
with open("trace.jsonl", "a") as f:
    f.write(json.dumps([v.model_dump() for v in verdicts]) + "\n")