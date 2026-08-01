import json
import re

from app.config import settings
from app.services.llm_client import LLMNotConfiguredError, get_client

SYSTEM_PROMPT = """You are a precise text summarizer. Given a piece of text, produce a
summary and a list of key points.

Respond with ONLY valid JSON, no markdown fences, in this exact shape:
{
  "summary": "the summary text",
  "key_points": ["point 1", "point 2"]
}

Rules:
- Never invent facts not present in the source text.
- Keep the summary faithful and concise.
- If style is "bullet", write the summary itself as short bullet-like sentences
  joined by newlines rather than one flowing paragraph.
- key_points should be the 3-6 most important standalone facts or takeaways."""


class SummarizationError(RuntimeError):
    pass


def _strip_code_fence(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def summarize_text(text: str, style: str, max_sentences: int) -> dict:
    try:
        client = get_client()
    except LLMNotConfiguredError as exc:
        raise SummarizationError(str(exc)) from exc

    user_prompt = (
        f"Style: {style}\nMax length: about {max_sentences} sentences\n\nText:\n{text}"
    )

    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=1536,
        )
    except Exception as exc:  # noqa: BLE001 — surfaced as a clean API error
        message = str(exc).split("\n")[0][:200]
        raise SummarizationError(f"Summarization request failed: {message}") from exc

    content = response.choices[0].message.content or "{}"
    try:
        parsed = json.loads(_strip_code_fence(content))
    except json.JSONDecodeError:
        parsed = {"summary": content.strip(), "key_points": []}

    summary = parsed.get("summary", "").strip()
    key_points = parsed.get("key_points", []) or []
    if not summary:
        raise SummarizationError("The model returned an empty summary.")

    return {"summary": summary, "key_points": key_points}
