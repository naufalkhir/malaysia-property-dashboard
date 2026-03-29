from fastapi import APIRouter
import plotly.express as px
from services.db import query_df
import os
import json

router = APIRouter(prefix="/charts", tags=["Charts"])

# Read DB driver from env — needed to handle SQL syntax differences
# MySQL uses DATE_FORMAT(), PostgreSQL uses TO_CHAR()
DRIVER = os.getenv("DB_DRIVER", "mysql")


def fig_to_json(fig):
    """
    Convert a Plotly figure object to a plain JSON dict.
    The Nuxt frontend receives this JSON and renders it with Plotly.js directly.
    This is the key integration between Python analytics and the Vue frontend.
    """
    return json.loads(fig.to_json())


# GET /charts/trends/{state}
# Price trend over time for a given Malaysian state
@router.get("/trends/{state}")
def trends(state: str):
    # PostgreSQL uses TO_CHAR() for date formatting, MySQL uses DATE_FORMAT()
    # We switch based on DB_DRIVER env variable
    if DRIVER == "postgresql":
        date_format = "TO_CHAR(listed_at, 'YYYY-MM') as month"
    else:
        date_format = "DATE_FORMAT(listed_at, '%Y-%m') as month"

    df = query_df(f"""
        SELECT 
            {date_format},
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
# Histogram showing how property prices are distributed across types
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
# Box plot showing price per sqft spread across states
# Box plot shows median, quartiles and outliers — better than just average
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
# Pie chart showing proportion of each property type in the dataset
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
# Affordability ratio = avg property price / (median income × 12)
# < 3 = affordable, 3-5 = moderate, 5-10 = seriously unaffordable, >10 = severely unaffordable
# This cross-analysis between Kaggle property data and DOSM income data is a key feature
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
        color_continuous_scale="RdYlGn_r"  # Red = unaffordable, Green = affordable
    )
    return fig_to_json(fig)