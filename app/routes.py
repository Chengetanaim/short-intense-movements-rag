from fastapi import APIRouter

from app.domain import create_rag_chain

router = APIRouter()

@router.get("/")
def ask_bot(input: str):
    rag_chain = create_rag_chain()
    result = rag_chain.invoke(input)
    return {"message": result}