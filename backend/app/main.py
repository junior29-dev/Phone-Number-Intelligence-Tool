from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .service import InvalidNumber, analyze

app = FastAPI(title="Phone Intel API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS, allow_methods=["GET"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/lookup")
def lookup(
    number: str = Query(..., min_length=3, max_length=32, description="Phone number, ideally with +country code"),
    region: str | None = Query(None, min_length=2, max_length=2, description="Default region (e.g. ZA) for local numbers"),
):
    try:
        return analyze(number, region.upper() if region else None)
    except InvalidNumber as exc:
        raise HTTPException(status_code=422, detail=str(exc))
