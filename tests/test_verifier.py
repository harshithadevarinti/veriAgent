from agents.schemas import Evidence
from agents.verifier import verify_claim, verify_with_retrieval


def fake_llm_supported(prompt: str) -> str:
    return '{"label": "SUPPORTED", "confidence": 0.9, "rationale": "Matches."}'


def fake_llm_garbage(prompt: str) -> str:
    return "not json at all"


def fake_retrieve(query: str, k: int):
    return [Evidence(text="Paris is the capital of France.",
                     source="wiki", score=0.95)]


def test_supported_verdict():
    ev = [Evidence(text="Paris is the capital of France.", source="wiki", score=0.95)]
    v = verify_claim("Paris is the capital of France.", ev, fake_llm_supported)
    assert v.label == "SUPPORTED"
    assert v.confidence == 0.9
    assert v.iterations == 1


def test_bad_output_falls_back():
    v = verify_claim("anything", [], fake_llm_garbage)
    assert v.label == "NOT_ENOUGH_INFO"
    assert v.confidence == 0.0


def test_loop_stops_when_confident():
    v = verify_with_retrieval("Paris is the capital of France.",
                              fake_retrieve, fake_llm_supported)
    assert v.iterations == 1


def test_loop_gives_up_after_max_iterations():
    v = verify_with_retrieval("anything", fake_retrieve, fake_llm_garbage)
    assert v.iterations == 3
    assert v.label == "NOT_ENOUGH_INFO"