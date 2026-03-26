from fastapi import APIRouter
import plotly.express as px
from services.db import query_df
import json

router = APIRouter(prefix="/charts", tags=["Charts"])

# Helper — converts Plotly figure to JSON dict
# Nuxt frontend will receive this JSON and render it directly with Plotly.js
def fig_to_json(fig):
    return json.loads(fig.to_json())

# GET /charts/trends/{state}
# Price trend over time for a given state
@router.get("/trends/{state}")
def trends(state: str):
    df = query_df(f"""
        SELECT 
            DATE_FORMAT(listed_at, '%Y-%m') as month,
            AVG(price) as avg_price,
            COUNT(*) as listing_count
        FROM properties
        WHERE state = '{state}' AND listed_at IS NOT NULL
        GROUP BY month
        ORDER BY month
    """)
    fig = px.line(
        df, x="month", y="avg_price",
        title=f"Average Price Trend — {state}",
        labels={"avg_price": "Average Price (MYR)", "month": "Month"}
    )
    return fig_to_json(fig)

# GET /charts/distribution
# Price distribution histogram
@router.get("/distribution")
def distribution():
    df = query_df("""
        SELECT price, property_type
        FROM properties
        WHERE price BETWEEN 50000 AND 5000000
    """)
    fig = px.histogram(
        df, x="price", color="property_type",
        title="Property Price Distribution",
        labels={"price": "Price (MYR)", "count": "Number of Listings"},
        nbins=50
    )
    return fig_to_json(fig)

# GET /charts/psf-by-state
# Price per sqft box plot by state
@router.get("/psf-by-state")
def psf_by_state():
    df = query_df("""
        SELECT state, price_per_sqft
        FROM properties
        WHERE price_per_sqft BETWEEN 50 AND 2000
    """)
    fig = px.box(
        df, x="state", y="price_per_sqft",
        title="Price per Sqft by State",
        labels={"price_per_sqft": "Price per Sqft (MYR)", "state": "State"}
    )
    return fig_to_json(fig)

# GET /charts/type-breakdown
# Property type pie chart
@router.get("/type-breakdown")
def type_breakdown():
    df = query_df("""
        SELECT property_type, COUNT(*) as count
        FROM properties
        GROUP BY property_type
        ORDER BY count DESC
    """)
    fig = px.pie(
        df, names="property_type", values="count",
        title="Property Type Breakdown"
    )
    return fig_to_json(fig)

# GET /charts/affordability-bar
# Affordability ratio bar chart by state
@router.get("/affordability-bar")
def affordability_bar():
    df = query_df("""
        SELECT 
            p.state,
            AVG(p.price) / (AVG(d.median_household_income) * 12) as affordability_ratio
        FROM properties p
        LEFT JOIN dosm_demographics d ON p.state = d.state
        WHERE d.year = (SELECT MAX(year) FROM dosm_demographics)
        GROUP BY p.state
        ORDER BY affordability_ratio DESC
    """)
    fig = px.bar(
        df, x="state", y="affordability_ratio",
        title="Housing Affordability Ratio by State",
        labels={"affordability_ratio": "Affordability Ratio", "state": "State"},
        color="affordability_ratio",
        color_continuous_scale="RdYlGn_r"
    )
    return fig_to_json(fig)