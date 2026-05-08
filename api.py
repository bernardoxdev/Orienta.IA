from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from contextlib import asynccontextmanager

from backend.core.limiter import limiter
from backend.events.register_events import register_events
from backend.routes.auth.auth import router as auth_router
from backend.routes.auth.auth_admin import router as auth_admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_events()

    yield

app = FastAPI(
    title="QuantFacial",
    summary="API de Sistema de Reconhecimento Facial para Controle de Acesso",
    description="",
    version="v0.1.0-BETA",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

app.include_router(auth_router)
app.include_router(auth_admin_router)

if __name__ == '__main__':
    pass