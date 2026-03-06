"""
Arthor Agent — FastAPI application.
PRD §5; docs/01-architecture-and-tech-stack.md.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import assessments, health, kb
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Shutdown: close KB/LLM resources if needed


app = FastAPI(
    title="Arthor Agent API",
    description="Arthor Agent — automated security assessment for documents and questionnaires. PRD-aligned.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(assessments.router, prefix=settings.API_PREFIX)
app.include_router(kb.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {"service": "Arthor Agent", "docs": "/docs", "health": "/health"}
