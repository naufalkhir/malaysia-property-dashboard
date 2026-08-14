from fastapi import APIRouter

from services.db import query_df

router = APIRouter(prefix="/stats", tags=["Stats"])


# GET /stats/affordability
# Joins property prices with DOSM income data to calculate affordability ratio
@router.get("/affordability")
def affordability():
    df = query_df("""
        SELECT 
            p.state,
            AVG(p.price) as avg_price,
            d.median_household_income,
            -- Affordability ratio = avg price / (monthly income x 12)
            AVG(p.price) / (d.median_household_income * 12) as affordability_ratio,
            COUNT(p.id) as listing_count
        FROM properties p
        LEFT JOIN dosm_demographics d ON p.state = d.state
        WHERE d.year = (SELECT MAX(year) FROM dosm_demographics)
        GROUP BY p.state, d.median_household_income
        ORDER BY affordability_ratio DESC
    """)
    return df.to_dict(orient="records")


# GET /stats/summary
# Overall market stats for dashboard KPI cards
@router.get("/summary")
def summary():
    df = query_df("""
        SELECT
            COUNT(*) as total_listings,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(price_per_sqft) as avg_price_psf
        FROM properties
    """)
    return df.to_dict(orient="records")[0]


# GET /stats/correlation
# Pearson correlation between numeric property features
@router.get("/correlation")
def correlation():
    df = query_df("""
        SELECT price, size_sqft, bedrooms, bathrooms, 
               car_parks, price_per_sqft
        FROM properties
        WHERE price IS NOT NULL AND size_sqft IS NOT NULL
    """)
    # .corr() computes correlation matrix — values between -1 and 1
    # 1 = perfect positive correlation, -1 = perfect negative, 0 = no relation
    corr = df.corr(numeric_only=True).round(3)
    return corr.to_dict()


# GET /stats/demographic
# Cross-analysis of property prices vs DOSM demographic data
@router.get("/demographic")
def demographic():
    df = query_df("""
        SELECT
            p.state,
            AVG(p.price) as avg_price,
            AVG(p.price_per_sqft) as avg_psf,
            COUNT(p.id) as listing_count,
            d.population,
            d.median_household_income,
            d.unemployment_rate,
            d.urbanisation_rate
        FROM properties p
        LEFT JOIN dosm_demographics d ON p.state = d.state
        WHERE d.year = (SELECT MAX(year) FROM dosm_demographics)
        GROUP BY p.state, d.population, d.median_household_income,
                 d.unemployment_rate, d.urbanisation_rate
        ORDER BY avg_price DESC
    """)
    return df.to_dict(orient="records")
