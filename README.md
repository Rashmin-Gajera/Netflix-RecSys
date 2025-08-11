# Netflix RecSys - Minimal Working Repo

<p align="center">
  <img src="https://img.shields.io/badge/Author-Rashmin%20Gajera-blue" alt="Author" />
  <img src="https://img.shields.io/badge/Open%20for%20Suggestions-Yes-brightgreen" alt="Open for Suggestions" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-Type-Recommendation%20System-red" alt="Project Type" />
</p>

---

## 🚀 Overview

Netflix RecSys is a modular, local-first Netflix-style movie recommendation system. It features:

- FastAPI backend
- Sentence-Transformers for embeddings
- ChromaDB for vector storage
- Reranking (cosine similarity, TensorFlow cross-encoder)
- LangChain for LLM explanations
- Simple HTML/JS frontend

---

## 🛠️ Tech Stack

<div align="center">
  <table>
    <tr>
      <td align="center" style="border-radius: 12px; border: 1px solid #eee; padding: 12px; margin: 6px;">
        <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white" alt="FastAPI" />
      </td>
      <td align="center" style="border-radius: 12px; border: 1px solid #eee; padding: 12px; margin: 6px;">
        <img src="https://img.shields.io/badge/Sentence%20Transformers-4B8BBE?logo=python&logoColor=white" alt="Sentence Transformers" />
      </td>
      <td align="center" style="border-radius: 12px; border: 1px solid #eee; padding: 12px; margin: 6px;">
        <img src="https://img.shields.io/badge/ChromaDB-13EF7C?logo=databricks&logoColor=white" alt="ChromaDB" />
      </td>
      <td align="center" style="border-radius: 12px; border: 1px solid #eee; padding: 12px; margin: 6px;">
        <img src="https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white" alt="TensorFlow" />
      </td>
      <td align="center" style="border-radius: 12px; border: 1px solid #eee; padding: 12px; margin: 6px;">
        <img src="https://img.shields.io/badge/Numpy-013243?logo=numpy&logoColor=white" alt="Numpy" />
      </td>
      <td align="center" style="border-radius: 12px; border: 1px solid #eee; padding: 12px; margin: 6px;">
        <img src="https://img.shields.io/badge/Selenium-43B02A?logo=selenium&logoColor=white" alt="Selenium" />
      </td>
      <td align="center" style="border-radius: 12px; border: 1px solid #eee; padding: 12px; margin: 6px;">
        <img src="https://img.shields.io/badge/LangChain-000000?logo=python&logoColor=white" alt="LangChain" />
      </td>
    </tr>
  </table>
</div>

---

## Directory & File Structure Overview

### Top-Level

- **[README.md](README.md)**  
  _This file. Project overview, file walkthrough, and credits._

- **[RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md)**  
  Step-by-step guide to running, training, and extending the system locally.

- **[docker-compose.yml](docker-compose.yml)**  
  Docker Compose setup for ChromaDB, API, and frontend services.

- **data/**  
  - **processed/sample_movies.jsonl**  
    Sample movie dataset (JSONL format) for ingestion and testing.

---

### services/

#### api/

- **requirements.txt**  
  All Python dependencies for the API service.

- **app/**  
  - **main.py**  
    FastAPI app entrypoint. Loads API routes and health check.
  - **api.py**  
    Registers and includes all API routers.
  - **routes/recommend.py**  
    `/api/recommend/query` endpoint: Accepts a query, retrieves candidates, reranks, and returns recommendations.

#### embeddings/

- **embedder.py**  
  Embedding pipeline using sentence-transformers. Also provides a CLI for ingesting data into ChromaDB.
- **requirements.txt**  
  Dependencies for embedding and ingestion.

#### retriever/

- **chroma_client.py**  
  ChromaDB client for upserting and searching movie vectors.
- **requirements.txt**  
  ChromaDB dependency.

#### reranker/

- **model.py**  
  Lightweight in-memory reranker using cosine similarity.
- **tf_crossencoder.py**  
  TensorFlow-based cross-encoder reranker (trainable, optional).
- **requirements.txt**  
  Numpy dependency for reranking.

#### scraper/

- **selenium_scraper.py**  
  Selenium-based IMDB plot fetcher (stub/example).
- **requirements.txt**  
  Selenium and requests dependencies.

#### langchain/

- **rag.py**  
  LangChain-based RAG pipeline for LLM-powered recommendation explanations.

#### frontend/

- **index.html**  
  Simple HTML/JS frontend for demoing the recommendation API.

---

## How It Works

1. **Ingest Data:**  
   Use [`services/embeddings/embedder.py`](services/embeddings/embedder.py) to encode movie plots and store them in ChromaDB.

2. **API Service:**  
   [`services/api/app/main.py`](services/api/app/main.py) launches a FastAPI server exposing `/api/recommend/query`.

3. **Retrieval & Reranking:**  
   - [`services/retriever/chroma_client.py`](services/retriever/chroma_client.py) retrieves candidates from ChromaDB.
   - [`services/reranker/model.py`](services/reranker/model.py) reranks candidates by similarity to the query.

4. **Frontend:**  
   [`services/frontend/index.html`](services/frontend/index.html) provides a simple UI to test recommendations.

5. **Optional Extensions:**  
   - [`services/reranker/tf_crossencoder.py`](services/reranker/tf_crossencoder.py): Trainable reranker.
   - [`services/langchain/rag.py`](services/langchain/rag.py): LLM-based explanations for recommendations.
   - [`services/scraper/selenium_scraper.py`](services/scraper/selenium_scraper.py): IMDB plot scraping utility.

---

## Contributing

This project is **open for suggestions and improvements**!  
Feel free to open issues or pull requests.

---

## Credits

Made by **Rashmin Gajera**.

---