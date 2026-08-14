import os

from fastapi import APIRouter, Depends, Header, HTTPException

from services.db import query_df

router = APIRouter(prefix="/etl", tags=["ETL"])


# Shared-secret check for destructive endpoints — same pattern as Laravel's
# X-API-Key middleware on /api/import/*. Read at request time (not import time)
# so tests can override the env var freely.
def verify_etl_api_key(x_api_key: str | None = Header(default=None)):
    expected = os.getenv("ETL_API_KEY")
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")

# GET /etl/quality-report
# Shows data quality stats — useful for admin/portfolio demo
@router.get("/quality-report")
def quality_report():
    df = query_df("""
        SELECT
            COUNT(*) as total_rows,
            SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) as null_price,
            SUM(CASE WHEN size_sqft IS NULL THEN 1 ELSE 0 END) as null_sqft,
            SUM(CASE WHEN lat IS NULL THEN 1 ELSE 0 END) as null_lat,
            SUM(CASE WHEN state IS NULL THEN 1 ELSE 0 END) as null_state,
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(price) as avg_price
        FROM properties
    """)
    return df.to_dict(orient="records")[0]

# POST /etl/clean/properties
# Removes outliers and bad data — destructive, so it requires ETL_API_KEY
@router.post("/clean/properties", dependencies=[Depends(verify_etl_api_key)])
def clean_properties():
    # Remove properties with clearly wrong prices
    query_df("""
        DELETE FROM properties
        WHERE price < 10000 OR price > 50000000
    """)
    # Remove properties with impossible sqft
    query_df("""
        DELETE FROM properties  
        WHERE size_sqft <= 0 OR size_sqft > 100000
    """)
    return {"message": "Data cleaned successfully"}