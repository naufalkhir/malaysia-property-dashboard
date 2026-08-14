import json
import os

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from fastapi import APIRouter

from services.db import query_df

router = APIRouter(prefix="/charts", tags=["Charts"])

# Switch SQL date formatting based on DB driver
# MySQL: DATE_FORMAT(col, '%Y-%m')
# PostgreSQL: TO_CHAR(col, 'YYYY-MM')
DRIVER = os.getenv("DB_DRIVER", "mysql")


# ─────────────────────────────────────────────
# Helper: same grouping used in train_model.py
# Keep this consistent so charts match ML model
# ─────────────────────────────────────────────
def simplify_type(t: str) -> str:
    t = str(t).lower()
    if any(x in t for x in ["condominium", "service residence", "apartment", "flat", "condo"]):
        return "High-Rise (Condo/Apt)"
    elif any(x in t for x in ["terrace", "link", "town house", "townhouse"]):
        return "Terrace / Town House"
    elif any(x in t for x in ["semi d", "semi-d", "cluster"]):
        return "Semi-D / Cluster"
    elif any(x in t for x in ["bungalow", "villa", "detached"]):
        return "Bungalow / Villa"
    else:
        return "Other"


# ─────────────────────────────────────────────
# 1. PRICE TREND
#
# Problem: listed_at is NULL for most rows, so
# grouping by month gives an empty chart.
#
# Fix: detect if we have real date data.
# - If yes → show avg price by month (original)
# - If no  → fallback to avg price by state (bar)
#   This gives a useful chart instead of blank.
# ─────────────────────────────────────────────
@router.get("/trends/{state}")
def price_trends(state: str):
    # Check how many rows actually have a date
    count_df = query_df("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN listed_at IS NOT NULL THEN 1 ELSE 0 END) as with_date
        FROM properties
        WHERE state = :state AND price > 0
    """, {"state": state})

    with_date = int(count_df["with_date"].iloc[0])

    # Need at least 3 months of data to draw a meaningful trend line
    has_date_data = with_date >= 3

    if has_date_data:
        # ── Original time-series chart ──
        date_expr = "TO_CHAR(listed_at, 'YYYY-MM')" if DRIVER == "postgresql" else "DATE_FORMAT(listed_at, '%Y-%m')"
        df = query_df(f"""
            SELECT
                {date_expr} AS month,
                AVG(price) AS avg_price,
                COUNT(*) AS listing_count
            FROM properties
            WHERE state = :state
              AND listed_at IS NOT NULL
              AND price > 0
            GROUP BY month
            ORDER BY month
        """, {"state": state})

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["month"],
            y=df["avg_price"],
            mode="lines+markers",
            name="Avg Price",
            line={"color": "#2563eb", "width": 2},
            marker={"size": 6},
            hovertemplate="Month: %{x}<br>Avg Price: MYR %{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            title=f"Average Price Trend — {state}",
            xaxis_title="Month",
            yaxis_title="Average Price (MYR)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font={"family": "DM Sans, sans-serif"},
            yaxis={"tickformat": ",.0f", "tickprefix": "MYR "},
            hovermode="x unified",
        )

    else:
        # ── Fallback: avg price by state (bar chart) ──
        # Useful even without date data — shows market position
        df = query_df("""
            SELECT
                state,
                AVG(price) AS avg_price,
                COUNT(*) AS listing_count
            FROM properties
            WHERE price > 0
            GROUP BY state
            ORDER BY avg_price DESC
        """)

        # Highlight the requested state in a different color
        colors = [
            "#2563eb" if s == state else "#cbd5e1"
            for s in df["state"]
        ]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["state"],
            y=df["avg_price"],
            marker_color=colors,
            hovertemplate="State: %{x}<br>Avg Price: MYR %{y:,.0f}<extra></extra>",
            name="Avg Price",
        ))
        fig.update_layout(
            # Tell the user why we're showing this instead
            title=f"Avg Price by State (no listing dates in DB — {state} highlighted)",
            xaxis_title="State",
            yaxis_title="Average Price (MYR)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font={"family": "DM Sans, sans-serif"},
            yaxis={"tickformat": ",.0f", "tickprefix": "MYR "},
            xaxis={"tickangle": -30},
        )

    return json.loads(fig.to_json() or '{}')


# ─────────────────────────────────────────────
# 2. PRICE DISTRIBUTION
#
# Problem: extreme outliers (RM 50M mansions)
# squash all the data to the left of the chart.
#
# Fix: filter to 5th–95th percentile before
# plotting. We show the realistic market range.
# Still show a note about removed outliers.
# ─────────────────────────────────────────────
@router.get("/distribution")
def price_distribution():
    df = query_df("""
        SELECT price, property_type
        FROM properties
        WHERE price > 0
    """)

    # Apply IQR outlier filter — same logic as train_model.py
    # This removes the extreme high-end properties that squash the chart
    q05 = df["price"].quantile(0.05)
    q95 = df["price"].quantile(0.95)
    df_filtered = df[(df["price"] >= q05) & (df["price"] <= q95)].copy()

    # Simplify property types for the legend (same 5 categories)
    df_filtered["category"] = df_filtered["property_type"].apply(simplify_type)

    removed_count = len(df) - len(df_filtered)

    # Color map for the 5 categories
    color_map = {
        "High-Rise (Condo/Apt)":  "#2563eb",
        "Terrace / Town House":   "#16a34a",
        "Semi-D / Cluster":       "#d97706",
        "Bungalow / Villa":       "#9333ea",
        "Other":                  "#94a3b8",
    }

    fig = px.histogram(
        df_filtered,
        x="price",
        color="category",
        nbins=50,
        color_discrete_map=color_map,
        labels={"price": "Price (MYR)", "category": "Property Type"},
        title=f"Property Price Distribution (5th–95th percentile, {removed_count} outliers removed)",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"family": "DM Sans, sans-serif"},
        xaxis={"tickformat": ",.0f", "tickprefix": "MYR "},
        yaxis_title="Number of Listings",
        bargap=0.05,
        legend={
            "title": "Property Type",
            "orientation": "v",
            "yanchor": "top",
            "y": 0.99,
            "xanchor": "right",
            "x": 0.99,
        },
    )
    return json.loads(fig.to_json() or '{}')


# ─────────────────────────────────────────────
# 3. PRICE PER SQFT BY STATE (box plot)
# No major issue here — just clean it up
# ─────────────────────────────────────────────
@router.get("/psf-by-state")
def psf_by_state():
    df = query_df("""
        SELECT state, price_per_sqft
        FROM properties
        WHERE price_per_sqft > 0
          AND price_per_sqft < 2000   -- remove extreme outliers
    """)

    # Sort states by median PSF descending so most expensive is first
    state_order = (
        df.groupby("state")["price_per_sqft"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )

    fig = go.Figure()
    for state in state_order:
        state_data = df[df["state"] == state]["price_per_sqft"]
        fig.add_trace(go.Box(
            y=state_data,
            name=state,
            boxpoints="outliers",     # only show outlier dots, not all points
            marker_color="#2563eb",
            line_color="#1d4ed8",
        ))

    fig.update_layout(
        title="Price per Sqft by State (MYR/sqft)",
        xaxis_title="State",
        yaxis_title="Price per Sqft (MYR)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"family": "DM Sans, sans-serif"},
        showlegend=False,
        xaxis={"tickangle": -30},
    )
    return json.loads(fig.to_json() or '{}')


# ─────────────────────────────────────────────
# 4. PROPERTY TYPE BREAKDOWN (pie chart)
#
# Problem: 50 tiny slices because every unique
# string in your DB becomes its own slice.
# "Terrace House, Semi D" and "Semi D, Terrace
# House" count as two different types.
#
# Fix: apply simplify_type() to group everything
# into 5 clean categories — same as ML model.
# ─────────────────────────────────────────────
@router.get("/type-breakdown")
def type_breakdown():
    df = query_df("""
        SELECT property_type, COUNT(*) as count
        FROM properties
        WHERE property_type IS NOT NULL
        GROUP BY property_type
    """)

    # Group messy types into 5 clean categories
    df["category"] = df["property_type"].apply(simplify_type)
    grouped = df.groupby("category")["count"].sum().reset_index()
    grouped = grouped.sort_values("count", ascending=False)

    color_map = {
        "High-Rise (Condo/Apt)":  "#2563eb",
        "Terrace / Town House":   "#16a34a",
        "Semi-D / Cluster":       "#d97706",
        "Bungalow / Villa":       "#9333ea",
        "Other":                  "#94a3b8",
    }
    colors = [color_map.get(c, "#94a3b8") for c in grouped["category"]]

    fig = go.Figure(go.Pie(
        labels=grouped["category"],
        values=grouped["count"],
        marker={"colors": colors},
        hole=0.35,              # donut style — looks cleaner than full pie
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="%{label}<br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig.update_layout(
        title="Property Type Breakdown (5 Categories)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"family": "DM Sans, sans-serif"},
        showlegend=True,
        legend={
            "orientation": "v",
            "yanchor": "middle",
            "y": 0.5,
            "xanchor": "left",
            "x": 1.02,
        },
        margin={"t": 60, "b": 60, "l": 60, "r": 160},  # extra right margin for legend
    )
    return json.loads(fig.to_json() or '{}')


# ─────────────────────────────────────────────
# 5. AFFORDABILITY BAR
# Fixed GROUP BY — same as before
# ─────────────────────────────────────────────
@router.get("/affordability-bar")
def affordability_bar():
    df = query_df("""
        SELECT
            p.state,
            AVG(p.price) / (AVG(d.median_household_income) * 12) AS affordability_ratio,
            AVG(p.price) AS avg_price,
            AVG(d.median_household_income) AS median_income
        FROM properties p
        LEFT JOIN dosm_demographics d ON p.state = d.state
        WHERE d.year = (SELECT MAX(year) FROM dosm_demographics)
          AND p.price > 0
          AND d.median_household_income > 0
        GROUP BY p.state
        ORDER BY affordability_ratio DESC
    """)

    df = df.replace({np.nan: None}).dropna(subset=["affordability_ratio"])

    # Color bars by affordability band:
    # < 3 = affordable (green), 3-5 = moderate (amber), 5-10 = serious (orange), >10 = severe (red)
    def bar_color(ratio):
        if ratio < 3:
            return "#16a34a"
        elif ratio < 5:
            return "#d97706"
        elif ratio < 10:
            return "#ea580c"
        else:
            return "#dc2626"

    colors = [bar_color(r) for r in df["affordability_ratio"]]

    fig = go.Figure(go.Bar(
        x=df["state"],
        y=df["affordability_ratio"],
        marker_color=colors,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Affordability Ratio: %{y:.1f}x<br>"
            "<extra></extra>"
        ),
    ))

    # Reference lines — standard Housing Affordability thresholds
    fig.add_hline(y=3,  line_dash="dot", line_color="#16a34a", annotation_text="Affordable (<3x)")
    fig.add_hline(y=5,  line_dash="dot", line_color="#d97706", annotation_text="Moderate (5x)")
    fig.add_hline(y=10, line_dash="dot", line_color="#dc2626", annotation_text="Severe (10x)")

    fig.update_layout(
        title="Housing Affordability by State (Price ÷ Annual Median Income)",
        xaxis_title="State",
        yaxis_title="Affordability Ratio (× annual income)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"family": "DM Sans, sans-serif"},
        xaxis={"tickangle": -30},
        showlegend=False,
    )
    return json.loads(fig.to_json() or '{}')