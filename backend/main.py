from fastapi import FastAPI
from pydantic import BaseModel
from report.generator import generate_report
from agents.pipeline import verify_response
from retriever.retriever import retrieve

app = FastAPI()


class CheckRequest(BaseModel):
    text: str


@app.post("/check")
def check_response(req: CheckRequest):
    verdicts = verify_response(req.text, retrieve)
    return generate_report(verdicts)