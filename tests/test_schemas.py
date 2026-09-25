from agents.schemas import Evidence, Verdict


def test_evidence():
    evidence = Evidence(
        text="The Earth is round.",
        source="Test Source",
        score=0.95
    )

    assert evidence.text == "The Earth is round."
    assert evidence.source == "Test Source"
    assert evidence.score == 0.95


def test_verdict():
    verdict = Verdict(
        claim="The Earth is round.",
        label="SUPPORTED",
        confidence=0.95,
        rationale="The evidence supports the claim.",
        evidence=[]
    )

    assert verdict.claim == "The Earth is round."
    assert verdict.label == "SUPPORTED"
    assert verdict.confidence == 0.95