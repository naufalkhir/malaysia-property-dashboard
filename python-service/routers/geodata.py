import json
import os

import numpy as np
import requests
from fastapi import APIRouter

from services.db import query_df

router = APIRouter(prefix="/geodata", tags=["Geodata"])

# Cache GeoJSON locally so we don't download it every time
GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "../malaysia.geojson")


def get_malaysia_geojson():
    """Download Malaysia state boundaries from GADM if not cached locally"""
    if os.path.exists(GEOJSON_PATH):
        with open(GEOJSON_PATH) as f:
            return json.load(f)

    # Download from GADM

    # Fallback — simplified Malaysia GeoJSON
    fallback_url = "https://raw.githubusercontent.com/longzheng/open-geojsonmaps/master/malaysia.json"

    try:
        response = requests.get(fallback_url, timeout=10)
        geojson = response.json()
        # Cache it locally
        with open(GEOJSON_PATH, "w") as f:
            json.dump(geojson, f)
        return geojson
    except Exception:  # noqa: BLE001 — best-effort fetch/cache; any failure here just falls back to None
        return None


# GET /geodata/choropleth
# Returns GeoJSON merged with property analytics per state
@router.get("/choropleth")
def choropleth():
    df = query_df("""
        SELECT
            p.state,
            AVG(p.price) as avg_price,
            AVG(p.price_per_sqft) as avg_psf,
            COUNT(p.id) as listing_count,
            AVG(p.price) / NULLIF(AVG(d.median_household_income) * 12, 0) as affordability_ratio
        FROM properties p
        LEFT JOIN dosm_demographics d ON p.state = d.state
        GROUP BY p.state
    """)
    
    # FIX: Replace NaN with None so FastAPI can serialize it to JSON null
    df = df.replace({np.nan: None})
    
    return df.to_dict(orient="records")


# GET /geodata/heatmap
# Returns lat/lng points for Leaflet heatmap layer
@router.get("/heatmap")
def heatmap():
    df = query_df("""
        SELECT lat, lng, price
        FROM properties
        WHERE lat IS NOT NULL 
        AND lng IS NOT NULL
        AND lat BETWEEN 1 AND 8
        AND lng BETWEEN 99 AND 120
        LIMIT 5000
    """)
    # Format: [[lat, lng, intensity], ...]
    records = df.values.tolist()
    return {"points": records}


# GET /geodata/states
# Returns center coordinates for each Malaysian state
@router.get("/states")
def states():
    return {
        "Selangor": {"lat": 3.0738, "lng": 101.5183},
        "Kuala Lumpur": {"lat": 3.1390, "lng": 101.6869},
        "Johor": {"lat": 1.9344, "lng": 103.3587},
        "Penang": {"lat": 5.4141, "lng": 100.3288},
        "Perak": {"lat": 4.5921, "lng": 101.0901},
        "Sabah": {"lat": 5.9788, "lng": 116.0753},
        "Sarawak": {"lat": 1.5533, "lng": 110.3592},
        "Kedah": {"lat": 6.1184, "lng": 100.3685},
        "Kelantan": {"lat": 6.1254, "lng": 102.2381},
        "Melaka": {"lat": 2.1896, "lng": 102.2501},
        "Negeri Sembilan": {"lat": 2.7258, "lng": 101.9424},
        "Pahang": {"lat": 3.8126, "lng": 103.3256},
        "Perlis": {"lat": 6.4449, "lng": 100.2048},
        "Terengganu": {"lat": 5.3117, "lng": 103.1324},
        "Putrajaya": {"lat": 2.9264, "lng": 101.6964},
        "Labuan": {"lat": 5.2831, "lng": 115.2308},
    }
