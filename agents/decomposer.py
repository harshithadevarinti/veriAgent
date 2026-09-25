# agents/decomposer.py
from .llm import ask_json

SYSTEM = """You extract atomic, verifiable factual claims from a text.
Rules:
- Each claim is one fact, self-contained (replace pronouns with the entity name).
- Skip opinions, questions, greetings, and vague statements.
- Keep the original meaning; do not add facts.
Output: {"claims": ["...", "..."]}"""

def decompose(response: str) -> list[str]:
    data = ask_json(SYSTEM, f"Text:\n{response}")
    return [c.strip() for c in data.get("claims", []) if c.strip()]