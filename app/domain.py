from functools import lru_cache
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from app.utils import document_text, format_docs

load_dotenv()


def build_vectorstore():
    """Chunk source document and initialize Chroma vector store with Gemini embeddings."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
    chunks = splitter.create_documents([document_text])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
    vectorstore = Chroma.from_documents(chunks, embeddings)
    return vectorstore


def build_rag_chain():
    """Build and return the complete RAG chain returning both answer and source citations."""
    vectorstore = build_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question using only the following context.
        If the answer isn't in the context, say you don't know.

        Context:
        {context}

        Question: {question}
        """
    )

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=lambda x: format_docs(x["context"]))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_sources = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    return rag_chain_with_sources


@lru_cache(maxsize=1)
def get_rag_chain():
    """Cached singleton accessor for the RAG chain to avoid re-embedding on every request."""
    return build_rag_chain()
