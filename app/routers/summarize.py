from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_api_key
from app.schemas import SummarizeRequest, SummarizeResponse
from app.services.summarizer import SummarizationError, summarize_text

router = APIRouter(prefix="/api", tags=["summarize"], dependencies=[Depends(require_api_key)])


@router.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest):
    try:
        result = summarize_text(payload.text, payload.style, payload.max_sentences)
    except SummarizationError as exc:
        raise HTTPException(502, str(exc)) from exc

    return SummarizeResponse(
        summary=result["summary"],
        key_points=result["key_points"],
        original_length=len(payload.text),
        summary_length=len(result["summary"]),
    )
