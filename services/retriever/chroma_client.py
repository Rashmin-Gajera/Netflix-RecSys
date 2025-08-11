
from chromadb import Client
from chromadb.config import Settings
import os

class ChromaClient:
    def __init__(self, persist_directory: str = "./data/chroma"):
        os.makedirs(persist_directory, exist_ok=True)
        # Use local duckdb+parquet implementation for persistence
        self.client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory))
        self.collection = self.client.get_or_create_collection(name="movies")

    def upsert(self, docs, vectors):
        ids = [str(d['id']) for d in docs]
        metadatas = [{k: d.get(k) for k in ("title","year","genres")} for d in docs]
        documents = [d.get("plot", "") for d in docs]
        self.collection.add(ids=ids, metadatas=metadatas, documents=documents, embeddings=vectors)

    def search(self, vector, k=10):
        # chroma returns a dictionary with lists inside
        res = self.collection.query(query_embeddings=[vector], n_results=k, include=["metadatas","documents","distances"])
        return res
