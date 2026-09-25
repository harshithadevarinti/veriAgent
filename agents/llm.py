# agents/llm.py  (replace the Anthropic parts; keep ask_json as is)
import json, re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
_client = genai.Client()               # reads GEMINI_API_KEY
MODEL = "gemini-3.5-flash-lite"       # confirm the exact name in AI Studio

def ask(system: str, user: str, max_tokens: int = 1000) -> str:
    resp = _client.models.generate_content(
        model=MODEL,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            temperature=0,
            max_output_tokens=max_tokens,
        ),
    )
    return resp.text or ""

def ask_json(system: str, user: str):
    """Ask for JSON only, strip code fences, and parse."""
    text = ask(system + "\nReturn ONLY valid JSON, no extra text.", user)
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    return json.loads(text)