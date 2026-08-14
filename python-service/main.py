from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import charts, etl, geodata, predictions, stats

# FastAPI app instance — this is the entry point for all requests
app = FastAPI(
    title="Malaysia Realty Analytics",
    description="ML predictions, charts, stats and geodata for Malaysia Realty Analyzer",
    version="1.0.0",
)

# CORS middleware — controls which origins (domains) can call this API
# Without this, browsers block cross-origin requests for security reasons
# Python service is internal (only called by Laravel), but we allow localhost for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",  # Laravel local dev
        "http://127.0.0.1:8000",  # Laravel local dev (alternate)
        "http://localhost:3000",  # Nuxt local dev
        "https://propertyanalytics.naufaldev.cloud",  # Production domain
    ],
    allow_methods=["*"],  # Allow GET, POST, PUT, DELETE etc
    allow_headers=["*"],  # Allow all request headers
)

# Register all routers — each router handles a group of related endpoints
# This is like Laravel's Route::prefix() groups
app.include_router(stats.router)  # /stats/*
app.include_router(charts.router)  # /charts/*
app.include_router(predictions.router)  # /predict/*
app.include_router(geodata.router)  # /geodata/*
app.include_router(etl.router)  # /etl/*


# Health check endpoint — useful to verify the service is running
@app.get("/")
def root():
    return {"status": "Malaysia Realty Python Service is running!"}
