
import numpy as np
from services.embeddings.embedder import Embedder

class ReRanker:
    def __init__(self):
        self.embedder = Embedder()

    def rerank(self, query_text, candidates, top_k=10):
        # candidates: dict returned from Chroma query
        docs = candidates.get("documents", [[]])[0]
        metadatas = candidates.get("metadatas", [[]])[0]
        if len(docs) == 0:
            return []
        # compute embeddings for query + docs
        vecs = self.embedder.embed([query_text] + docs)
        qvec = vecs[0]
        dvecs = np.vstack(vecs[1:])
        # cosine similarity
        dnorm = np.linalg.norm(dvecs, axis=1)
        qnorm = np.linalg.norm(qvec) + 1e-12
        sims = (dvecs @ qvec) / (dnorm * qnorm + 1e-12)
        ranked_idx = np.argsort(-sims)
        out = []
        for i in ranked_idx[:top_k]:
            out.append({"title": metadatas[i].get("title",""), "score": float(sims[i])})
        return out
