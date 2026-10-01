from fastapi import APIRouter
from app.domain import get_rag_chain
from app.schemas import QueryRequest, QueryResponse, DocumentSource

router = APIRouter()


@router.post(
    "/api/v1/query",
    response_model=QueryResponse,
    summary="Ask a question to the RAG Assistant",
    description="Accepts a query, retrieves semantically relevant context chunks, and generates a grounded response with source citations.",
)
def query_rag(payload: QueryRequest):
    rag_chain = get_rag_chain()
    result = rag_chain.invoke(payload.query)

    sources = [
        DocumentSource(content=doc.page_content)
        for doc in result.get("context", [])
    ]

    return QueryResponse(
        query=payload.query,
        answer=result.get("answer", ""),
        sources=sources,
    )


@router.get(
    "/",
    summary="Health check & API info",
)
def root():
    return {
        "status": "healthy",
        "service": "Short Intense Movements RAG API",
        "docs_url": "/docs",
    }