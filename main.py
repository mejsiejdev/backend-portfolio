#import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from database import supabase  # noqa: E402
from core.redis import initialize_redis_pool, close_redis_pool, get_redis  # noqa: E402
from certificates import router as certificates_router  # noqa: E402
from projects import router as projects_router  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_redis_pool()
    yield
    await close_redis_pool()


# origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(certificates_router)
app.include_router(projects_router)


@app.get("/health")
async def health_check():
    health = {
        "status": "healthy",
        "services": {"database": "healthy", "redis": "healthy"},
    }
    try:
        supabase.table("projects").select("id").limit(1).execute()
    except Exception as e:
        health["services"]["database"] = f"error: {e}"
        health["status"] = "degraded"
    try:
        redis = get_redis()
        await redis.ping()
    except Exception as e:
        health["services"]["redis"] = f"error: {e}"
        health["status"] = "degraded"

    if health["status"] != "healthy":
        raise HTTPException(status_code=503, detail=health)
    return health
