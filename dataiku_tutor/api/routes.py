"""FastAPI route definitions for query and index management endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel, Field


class QueryPayload(BaseModel):
    question: str = Field(..., description="User question about Dataiku workflows")
    top_k: int = Field(default=5, ge=1, le=20)
    mode: str = Field(default="hybrid", pattern="^(semantic|keyword|hybrid)$")


class QueryResult(BaseModel):
    answer: str
    sources: list[dict]


class ReindexResult(BaseModel):
    indexed_chunks: int
    status: str


def build_router(tutor_service, index_updater) -> APIRouter:
    """Create API router with injected application services."""
    router = APIRouter()

    @router.post("/query", response_model=QueryResult)
    def query(payload: QueryPayload) -> QueryResult:
        raise NotImplementedError

    @router.post("/reindex", response_model=ReindexResult)
    def reindex() -> ReindexResult:
        raise NotImplementedError

    return router
