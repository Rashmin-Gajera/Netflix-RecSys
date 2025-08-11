# Netflix RecSys - Minimal Working Repo

**Author:** Rashmin Gajera  
**Open for suggestions and improvements!**

This repository is a runnable scaffold for a Netflix-style Recommendation System. It demonstrates a modular, local-first approach to building a movie recommendation pipeline using FastAPI, sentence-transformers, ChromaDB, reranking, and more.

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