
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.retriever.chroma_client import ChromaClient
from services.embeddings.embedder import Embedder
from services.reranker.model import ReRanker

router = APIRouter()

class RecRequest(BaseModel):
    query: str
    top_k: int = 10

# singletons for performance
_embedder = Embedder()
_chroma = ChromaClient()
_reranker = ReRanker()

@router.post("/query")
async def recommend(req: RecRequest):
    emb = _embedder.embed(req.query)[0]
    candidates = _chroma.search(emb, k=50)
    reranked = _reranker.rerank(req.query, candidates, top_k=req.top_k)  # returns top_k
    return {"recommendations": reranked}
