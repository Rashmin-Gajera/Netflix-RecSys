
# Follow Steps to run in your local device

1. Create and activate a Python virtualenv (Python 3.10+ recommended):
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate

2. Install API and embeddings requirements:
   pip install -r services/api/requirements.txt
   pip install -r services/embeddings/requirements.txt
   pip install -r services/retriever/requirements.txt

3. (Optional) Start Chroma via Docker Compose (if you want external Chroma service):
   docker-compose up -d chroma
   # or start full stack: docker-compose up -d

4. Ingest sample data into local Chroma/duckdb storage:
   python services/embeddings/embedder.py --input data/processed/sample_movies.jsonl
   This encodes the sample plots and stores them in ./data/chroma (duckdb+parquet)

5. Start the API:
   uvicorn services.api.app.main:app --reload --host 0.0.0.0 --port 8000
   The API will be available at http://localhost:8000

6. (Optional) Open the frontend demo:
   If running locally without Docker, you can open services/frontend/index.html in your browser
   OR use the bundled nginx image in docker-compose (frontend mapped to port 3000)

# TensorFlow Reranker (train + inference)

- To train a TensorFlow cross-encoder, install TensorFlow and Transformers (already included in requirements).
- Prepare a dataset of (query, doc, score) triples. See services/reranker/tf_crossencoder.py for training API.
- Example:
    from services.reranker.tf_crossencoder import TFReranker
    r = TFReranker(model_name='distilbert-base-uncased')
    dataset = [('dream-manipulation', 'Inception plot ...', 1.0), ('dream-manipulation', 'The Matrix plot ...', 0.3)]
    r.train(dataset, epochs=1)

# LangChain RAG integration

- Set OPENAI_API_KEY in your environment to enable explanation generation via OpenAI:
    export OPENAI_API_KEY=sk-...
- Use services/langchain/rag.py to build a vectordb and LLM chain. Example:
    from services.langchain.rag import build_rag, explain_recommendations
    vectordb, chain = build_rag(chain_api_key=os.environ.get('OPENAI_API_KEY'))
    print(explain_recommendations(chain, vectordb, 'mind-bending sci-fi about dreams', top_k=3))

# Notes on production tuning (latency <400ms)

- Keep embedder and reranker models warm in memory (load on service start).
- Use Faiss-backed vector index for high throughput via Chroma hybrid mode.
- Cache top-N results for common queries in Redis.
- Serve models with GPU and batch requests for heavy workloads.
