import json
from pathlib import Path
from typing import Iterator
from pydantic import BaseModel


class FeverExample(BaseModel):
    claim: str
    label: str          # SUPPORTS / REFUTES / NOT ENOUGH INFO
    evidence: list       # raw evidence sets from FEVER


class HaluEvalExample(BaseModel):
    task: str            # qa / dialogue / summarization
    input_text: str
    output_text: str
    is_hallucination: bool


class RagTruthExample(BaseModel):
    source: str
    response: str
    is_hallucination: bool
    hallucination_spans: list = []


def load_fever(path: str) -> Iterator[FeverExample]:
    """FEVER is distributed as JSONL: one claim per line."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            yield FeverExample(
                claim=row["claim"],
                label=row["label"],
                evidence=row.get("evidence", []),
            )


def load_halueval(path: str, task: str) -> Iterator[HaluEvalExample]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            yield HaluEvalExample(
                task=task,
                input_text=row.get("question", row.get("dialogue_history", "")),
                output_text=row.get("hallucinated_answer", row.get("output", "")),
                is_hallucination=True,
            )


def load_ragtruth(path: str) -> Iterator[RagTruthExample]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for row in data:
        yield RagTruthExample(
            source=row["source_info"],
            response=row["response"],
            is_hallucination=bool(row.get("labels")),
            hallucination_spans=row.get("labels", []),
        )