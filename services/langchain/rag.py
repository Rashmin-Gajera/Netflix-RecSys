
"""LangChain RAG pipeline integrating ChromaDB and an LLM for explanation generation.

Requires: langchain, openai (or another LLM connector), chromadb.
Set OPENAI_API_KEY in environment to use OpenAI LLM.
"""
from typing import List
import os

try:
    from langchain import OpenAI, LLMChain, PromptTemplate
    from langchain.vectorstores import Chroma
    from langchain.embeddings import HuggingFaceEmbeddings
except Exception as e:
    # Keep imports optional for static viewing
    OpenAI = None
    LLMChain = None
    PromptTemplate = None
    Chroma = None
    HuggingFaceEmbeddings = None

def build_rag(chain_api_key: str = None, chroma_persist_dir: str = './data/chroma'):
    if OpenAI is None:
        raise ImportError('langchain and an LLM client are required. pip install langchain openai')

    # Use HuggingFaceEmbeddings or OpenAI embeddings depending on availability
    hf_embed = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
    vectordb = Chroma(persist_directory=chroma_persist_dir, embedding_function=hf_embed)

    # Simple prompt template that provides retrieved contexts and asks the LLM to explain why a movie is recommended
    prompt = PromptTemplate(template='''You are an assistant that explains movie recommendations.
Given the user query: "{query}"
And the retrieved movie candidates with short plots:
{contexts}
Provide top {top_k} recommendations with a 1-2 sentence explanation for each.''',
                            input_variables=['query','contexts','top_k'])

    llm = OpenAI(temperature=0.2, openai_api_key=chain_api_key)
    chain = LLMChain(llm=llm, prompt=prompt)
    return vectordb, chain

def explain_recommendations(chain, vectordb, query: str, top_k: int = 5):
    # retrieve contexts
    docs = vectordb.similarity_search(query, k=top_k)
    contexts = '\n'.join([f"- {d.metadata.get('title','')} : {d.page_content[:200]}" for d in docs])
    resp = chain.run({'query': query, 'contexts': contexts, 'top_k': top_k})
    return resp
