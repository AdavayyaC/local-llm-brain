from fastapi import FastAPI
from app.utils.logging import setup_logger
from app.api.chat import router as chat_router

logger = setup_logger()

app = FastAPI(
    title="Local LLM Brain",
    description="CPU-only local LLM brain service",
    version="0.1.0"
)

app.include_router(chat_router)

@app.get("/")
def health_check():
    logger.info("Health check called")
    return {"status": "ok"}
