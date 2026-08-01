from typing import Literal

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=50000, description="The text to summarize.")
    style: Literal["paragraph", "bullet"] = Field("paragraph", description="Summary format.")
    max_sentences: int = Field(5, ge=1, le=20, description="Approximate max length of the summary.")


class SummarizeResponse(BaseModel):
    summary: str
    key_points: list[str]
    original_length: int
    summary_length: int
