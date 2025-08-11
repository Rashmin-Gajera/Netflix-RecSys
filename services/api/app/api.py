
from fastapi import APIRouter
from services.api.app.routes.recommend import router as rec_router

router = APIRouter()
router.include_router(rec_router, prefix="/recommend")
