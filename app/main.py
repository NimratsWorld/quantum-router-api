import time
import logging
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.security import limiter
from app.routers import router, insights, orchestrator

app = FastAPI(title="Quantum API Factory", version="1.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router.router, prefix="/api/v1")
app.include_router(insights.router, prefix="/api/v1")
app.include_router(orchestrator.router, prefix="/api/v1")

@app.get("/", tags=["System"])
def root():
    return {"status": "online", "factory": "Quantum-API"}