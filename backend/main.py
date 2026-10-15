from fastapi import FastAPI
from pydantic import BaseModel
from report.generator import generate_report
from agents.schemas import Verdict, Evidence

app = FastAPI()


class CheckRequest(BaseModel):
    text: str


@app.post("/check")
def check_response(req: CheckRequest):
    # TEMP: fake verdicts until Member 2's orchestrator is ready
    verdicts = [
        Verdict(
            claim="The Eiffel Tower is in Paris.",
            label="SUPPORTED",
            confidence=0.95,
            rationale="Matches evidence directly.",
            evidence=[Evidence(text="The Eiffel Tower is located in Paris, France.", source="wiki", score=0.9)],
            iterations=1,
        ),
        Verdict(
            claim="The Great Wall of China is visible from the Moon.",
            label="REFUTED",
            confidence=0.88,
            rationale="Contradicted by evidence; not visible to the naked eye from space.",
            evidence=[Evidence(text="Astronauts have confirmed the Great Wall is not visible from the Moon with the naked eye.", source="nasa", score=0.85)],
            iterations=1,
        ),
    ]
    return generate_report(verdicts)