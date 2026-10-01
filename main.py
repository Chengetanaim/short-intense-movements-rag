from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.domain import get_rag_chain
from app.routes import router as main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-warm the RAG chain and Chroma vector store during application startup
    try:
        get_rag_chain()
    except Exception as e:
        print(f"Warning: RAG initialization deferred or encountered issue: {e}")
    yield


app = FastAPI(
    title="Short-Intense-Movements RAG API",
    description="Domain-Specific RAG Knowledge Assistant & REST API powered by LangChain, Google Gemini, and ChromaDB.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)