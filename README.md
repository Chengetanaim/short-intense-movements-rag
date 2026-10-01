# Short-Intense-Movements RAG Assistant

> A high-performance, domain-specific Retrieval-Augmented Generation (RAG) backend and REST API built with **FastAPI**, **LangChain**, **Google Gemini**, and **ChromaDB**.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C?style=flat)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash%20%26%20Embeddings-8E75B2?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-blue?style=flat)](https://www.trychroma.com/)

---

## Overview

Organizations and researchers often struggle to extract accurate, fact-grounded insights from dense scientific literature. Generic LLMs without grounding frequently hallucinate or miss domain specifics.

This project implements an end-to-end RAG system specialized in **exercise physiology and high-intensity interval health research** (e.g., studies from *Cell Reports Medicine* and *Nature Medicine*). It indexes scientific text into a Chroma vector store using Google Gemini embeddings and answers queries through a constrained Gemini LLM pipeline.

---

## Key Features

- **Strict Anti-Hallucination Grounding:** Custom prompt design enforcing zero-extrapolation constraints — the assistant answers strictly using the verified retrieved context or explicitly states uncertainty.
- **Source Document Attribution & Citations:** Every response includes the retrieved source passages alongside the answer for full auditability and transparency.
- **Pre-warmed Vector Store & Singleton Chain:** Avoids re-embedding on every query by initializing the Chroma vector store and LCEL chain on startup.
- **Type-Safe Pydantic Schemas:** Fully validated request/response bodies with interactive OpenAPI/Swagger documentation.
- **Optimized Text Chunking:** Employs `RecursiveCharacterTextSplitter` tuned for medical/scientific abstracts to preserve semantic continuity across paragraph boundaries.
- **FastAPI Backend:** High-performance asynchronous REST endpoints ready for client integrations or web/mobile frontends.

---

## Architecture

```mermaid
flowchart LR
    A[Client Query / POST] --> B[FastAPI /api/v1/query]
    B --> C[Singleton RAG Chain]
    C -->|Embed Query| D[Google Gemini Embeddings]
    D -->|Similarity Search| E[(ChromaDB Vector Store)]
    E -->|Top-k Source Chunks| C
    C -->|Context + Question| F[Google Gemini 3.5 Flash-Lite]
    F -->|Grounded Answer + Citations| B
    B -->|Pydantic JSON Response| A
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google AI Studio API Key ([Get one here](https://aistudio.google.com/))

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Chengetanaim/short-intense-movements-rag.git
   cd short-intense-movements-rag
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY="your-gemini-api-key-here"
   ```

### 3. Running the API

Start the FastAPI development server:
```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

---

## 📡 API Usage & Examples

### Interactive Documentation
FastAPI automatically provides interactive Swagger docs:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Example Request (`POST /api/v1/query`)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What did the Cell Reports Medicine study find about plasma proteins?"}'
```

### Example Response
```json
{
  "query": "What did the Cell Reports Medicine study find about plasma proteins?",
  "answer": "The Cell Reports Medicine study found that among 2,884 plasma proteins measured, the high-intensity group showed increases in 714 proteins related to growth hormones, vascular function, tissue remodeling, and fat metabolism, compared to only 7 proteins in the moderate-intensity group.",
  "sources": [
    {
      "content": "A study recently published in the international journal *Cell Reports Medicine* explained the reason at the molecular level. Researchers divided 19 young, healthy men into two groups..."
    },
    {
      "content": "Among 2,884 plasma proteins measured, the high-intensity group showed increases in 714 proteins. These included growth hormones and substances related to vascular function..."
    }
  ]
}
```

---

## Project Structure

```text
├── app/
│   ├── domain.py      # LangChain RAG pipeline, Chroma vector store & singleton chain
│   ├── routes.py      # FastAPI route definitions (POST /api/v1/query)
│   ├── schemas.py     # Pydantic request and response models
│   └── utils.py       # Knowledge base documents and formatting helpers
├── main.py            # FastAPI entrypoint with lifespan pre-warming
├── .env.example       # Example environment variables
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

---

## License
Distributed under the MIT License.
