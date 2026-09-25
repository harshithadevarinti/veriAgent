import json
from typing import Callable, List
from agents.schemas import Evidence, Verdict

MAX_ITERATIONS = 3
CONFIDENCE_THRESHOLD = 0.7

PROMPT_TEMPLATE = """You are a fact-checking assistant.
Given a claim and evidence passages, decide whether the evidence
SUPPORTS the claim, REFUTES it, or is NOT_ENOUGH_INFO.

Respond ONLY with JSON in this exact form:
{{"label": "SUPPORTED|REFUTED|NOT_ENOUGH_INFO",
  "confidence": <float 0-1>,
  "rationale": "<one or two sentences>"}}

Claim: {claim}

Evidence:
{evidence}
"""


def _format_evidence(evidence: List[Evidence]) -> str:
    return "\n".join(
        f"[{i}] ({e.source}, score={e.score:.2f}) {e.text}"
        for i, e in enumerate(evidence, start=1)
    )


def _parse(raw: str) -> dict:
    """Parse LLM output. Returns a NOT_ENOUGH_INFO fallback on failure."""
    try:
        data = json.loads(raw.strip().removeprefix("```json").removesuffix("```"))
        label = data["label"]
        if label not in {"SUPPORTED", "REFUTED", "NOT_ENOUGH_INFO"}:
            raise ValueError(f"bad label: {label}")
        confidence = min(max(float(data["confidence"]), 0.0), 1.0)
        return {"label": label, "confidence": confidence,
                "rationale": str(data.get("rationale", ""))}
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        return {"label": "NOT_ENOUGH_INFO", "confidence": 0.0,
                "rationale": "Could not parse model output."}


def verify_claim(
    claim: str,
    evidence: List[Evidence],
    llm: Callable[[str], str],
    iteration: int = 1,
) -> Verdict:
    """Single verification pass. `llm` takes a prompt and returns text."""
    prompt = PROMPT_TEMPLATE.format(claim=claim, evidence=_format_evidence(evidence))
    result = _parse(llm(prompt))
    return Verdict(
        claim=claim,
        label=result["label"],
        confidence=result["confidence"],
        rationale=result["rationale"],
        evidence=evidence,
        iterations=iteration,
    )


def verify_with_retrieval(
    claim: str,
    retrieve: Callable[[str, int], List[Evidence]],
    llm: Callable[[str], str],
) -> Verdict:
    """Iterative loop: retrieve more evidence with each round until confident.

    `retrieve(query, k)` is supplied by Member 1. On round n we ask for
    more passages (k grows each round) so the model sees fresh context.
    """
    evidence: List[Evidence] = []
    verdict = None
    for iteration in range(1, MAX_ITERATIONS + 1):
        k = 5 * iteration
        evidence = retrieve(claim, k)
        verdict = verify_claim(claim, evidence, llm, iteration=iteration)
        if verdict.label != "NOT_ENOUGH_INFO" and verdict.confidence >= CONFIDENCE_THRESHOLD:
            break
    return verdict