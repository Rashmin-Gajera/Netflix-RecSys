
from fastapi import FastAPI
from services.api.app.api import router as api_router

app = FastAPI(title="Netflix RecSys API")
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}
