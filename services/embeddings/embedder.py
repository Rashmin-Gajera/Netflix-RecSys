
#!/usr/bin/env python3
import argparse, json
from sentence_transformers import SentenceTransformer
from services.retriever.chroma_client import ChromaClient
import numpy as np

class Embedder:
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        single = False
        if isinstance(texts, str):
            texts = [texts]
            single = True
        vecs = self.model.encode(texts, show_progress_bar=False)
        if single:
            return [vecs[0]]
        return vecs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSONL file with docs: {id, title, plot, year, genres}")
    args = parser.parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        docs = [json.loads(l) for l in f]
    embedder = Embedder()
    texts = [d.get("plot","") or d.get("title","") for d in docs]
    vectors = embedder.embed(texts)
    chroma = ChromaClient()
    chroma.upsert(docs, vectors)
    print(f"Ingested {len(docs)} docs into Chroma.")
