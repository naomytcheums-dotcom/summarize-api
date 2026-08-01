# Summarize API

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI_SDK-412991?style=flat&logo=openai&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white)

**[Live API](https://summarize-api-87y8.onrender.com)** — try it interactively at **[/docs](https://summarize-api-87y8.onrender.com/docs)**

A small, focused REST API: send it text, get back a concise summary and a list of key points. Built as a standalone backend service — no frontend, no database. Interactive documentation (Swagger UI) is generated automatically by FastAPI, so the API is self-documenting out of the box.

## Endpoint

### `POST /api/summarize`

**Headers**
- `X-API-Key` — required only if `API_ACCESS_KEY` is set on the server
- `Content-Type: application/json`

**Body**
```json
{
  "text": "The text you want summarized...",
  "style": "paragraph",
  "max_sentences": 5
}
```

- `text` — required, 1 to 50,000 characters
- `style` — `"paragraph"` or `"bullet"`, defaults to `"paragraph"`
- `max_sentences` — approximate target length, 1 to 20, defaults to 5

**Response**
```json
{
  "summary": "...",
  "key_points": ["...", "..."],
  "original_length": 512,
  "summary_length": 187
}
```

**Errors**
- `422` — invalid request body (missing/empty text, out-of-range values)
- `401` — missing or invalid `X-API-Key` (only if access control is enabled)
- `502` — the LLM request failed (quota, network, misconfigured key) — the response includes a clean, truncated reason

### `GET /api/health`

Returns `{"status": "ok"}`. Useful for uptime checks.

### `GET /docs`

Interactive Swagger UI — try the API directly from your browser.

## Example

```bash
curl -X POST https://summarize-api-87y8.onrender.com/api/summarize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key-if-set" \
  -d '{"text": "Long article text here...", "style": "bullet", "max_sentences": 4}'
```

## Tech stack

FastAPI, Pydantic, OpenAI-compatible LLM client (works with OpenAI, Google Gemini, Groq, or any OpenAI-compatible endpoint).

## Running locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in your own LLM key
uvicorn app.main:app --reload --port 8095
```

Then open `http://localhost:8095/docs` to try it interactively.

## Deploying

**Render:**
- New Web Service, root directory: repo root (no subfolder)
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables: `LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`, `API_ACCESS_KEY` (optional), `CORS_ORIGINS`

No frontend, no database — this is a pure backend API, deployable on its own.

## Status

This is an MVP built for portfolio purposes. It requires your own LLM API key — no credentials are shared or included. `API_ACCESS_KEY` is optional; leave it empty for an open demo, or set it to require callers to authenticate.
