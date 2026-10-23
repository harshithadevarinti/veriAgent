from agents.schemas import Verdict
def _clean_source(source: str) -> str:
    return source.replace("-LRB-", "(").replace("-RRB-", ")")


def generate_report(verdicts: list[Verdict]) -> dict:
    total = len(verdicts)
    supported = sum(1 for v in verdicts if v.label == "SUPPORTED")
    refuted = sum(1 for v in verdicts if v.label == "REFUTED")
    nei = total - supported - refuted

    overall_score = supported / total if total else 0.0

    return {
        "overall_score": round(overall_score, 3),
        "summary": {"SUPPORTED": supported, "REFUTED": refuted, "NOT_ENOUGH_INFO": nei},
        "claims": [
            {
                "claim": v.claim,
                "label": v.label,
                "confidence": v.confidence,
                "rationale": v.rationale,
                "evidence": [
                    {"text": e.text, "source": _clean_source(e.source), "score": e.score}
                    for e in v.evidence
                ],
            }
            for v in verdicts
        ],
    }