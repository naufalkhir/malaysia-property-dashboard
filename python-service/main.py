from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import stats, charts, predictions, geodata, etl

app = FastAPI(
    title="Malaysia Realty Analytics",
    description="ML predictions, charts, stats and geodata for Malaysia Realty Analyzer",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats.router)
app.include_router(charts.router)
app.include_router(predictions.router)
app.include_router(geodata.router)
app.include_router(etl.router)


@app.get("/")
def root():
    return {"status": "Malaysia Realty Python Service is running!"}
