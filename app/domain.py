from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.utils import document_text, format_docs

load_dotenv()


def create_rag_chain():

    splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    chunks = splitter.create_documents([document_text])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
    vectorstore = Chroma.from_documents(chunks, embeddings)

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

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

rag_chain = create_rag_chain()

