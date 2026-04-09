# 🇲🇾 Malaysia Realty Analyzer

A full-stack property analytics platform combining real Malaysian real estate listings with official government demographic data — featuring interactive maps, Plotly-powered charts, and a live ML price predictor.

> **Live Demo:** https://propertyanalytics.naufaldev.cloud  
> **Portfolio project** by [Muhammad Naufal](https://github.com/naufalkhir) · Selangor, Malaysia

![Laravel](https://img.shields.io/badge/Laravel-12-FF2D20?style=flat&logo=laravel&logoColor=white)
![Nuxt](https://img.shields.io/badge/Nuxt-3-00DC82?style=flat&logo=nuxt.js&logoColor=white)
![Python](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)

---

## 📸 Screenshots

> Add screenshots here after taking them

---

## 🏗️ Architecture

Three independent services in a monorepo, deployed on a single VPS behind Nginx:

```
Browser
  │
  └── Nginx (SSL termination + routing)
        ├── /          → Nuxt 3 Frontend     :3000  (SSR/CSR/SSG hybrid)
        └── /api/*     → Laravel 12 API      :8000
                             │
                             └── Python FastAPI    :8001  (internal only)
                             └── PostgreSQL 16     :5432  (internal only)
```

**Key architectural decision:** The frontend only ever talks to Laravel. Laravel proxies analytics requests to Python internally. Python is never exposed to the internet — it lives on a private Docker network.

### Services

| Service      | Tech                              | Port | Exposed          |
| ------------ | --------------------------------- | ---- | ---------------- |
| Frontend     | Nuxt 3 + Pinia + Leaflet + Plotly | 3000 | Via Nginx only   |
| Backend API  | Laravel 12 + Sanctum              | 8000 | Via Nginx `/api` |
| Analytics/ML | Python FastAPI + Scikit-learn     | 8001 | Internal only    |
| Database     | PostgreSQL 16                     | 5432 | Internal only    |

---

## ✨ Features

**Public pages (SSR — Google-indexed)**

- Property listings grid with filters (state, type, tenure, bedrooms, price range)
- Sortable, paginated (20/page)
- Individual property detail page with similar listings

**Analytics Dashboard (CSR)**

- KPI overview: total listings, avg price, top states
- 5 Plotly charts: price trends, distribution histogram, PSF box plot, type breakdown, affordability bar
- Demographic cross-analysis: median income vs property prices by state (DOSM data)
- Affordability ratio by state (price ÷ annual median income) with color-coded thresholds

**Interactive Map**

- Leaflet choropleth: Malaysian states coloured by average price/sqft
- Property heatmap layer
- Click state → popup with state summary

**ML Price Predictor**

- Inputs: state, property type, sqft, bedrooms, bathrooms
- Returns: predicted price + confidence interval (low/high range)
- Displays model accuracy stats (MAE, R²) alongside every prediction

---

## 🧠 Machine Learning

### Pipeline

```
PostgreSQL DB (58,531 rows)
  │
  ├── KL Property Listings    — 52,425 rows (Kaggle)
  ├── Malaysia House Prices   — ~3,000 rows (Kaggle)
  ├── DOSM demographics       — median income by state
  │
  └── train_model.py
        ├── JOIN properties + demographics on state
        ├── Feature engineering: One-Hot Encoding (state, property_category)
        ├── Numeric features: income_mean, income_median, size_sqft,
        │                     bedrooms, bathrooms, car_parks
        ├── Outlier removal: IQR method (10th–90th percentile)
        ├── Train RandomForestRegressor (300 estimators, max_depth=25)
        └── Save → price_model.pkl
```

### Results

| Metric        | Value           | Notes                                  |
| ------------- | --------------- | -------------------------------------- |
| R²            | **0.836**       | Model explains 83.6% of price variance |
| MAE           | MYR 277,861     | Average prediction error               |
| Training rows | ~38,782         | After IQR outlier removal              |
| Top feature   | size_sqft (82%) | Dominant predictor                     |

---

## 🗄️ Data Sources

| Source                                                                                 | Dataset                         | Rows    | License             |
| -------------------------------------------------------------------------------------- | ------------------------------- | ------- | ------------------- |
| [Kaggle](https://www.kaggle.com/datasets/dragonduck/property-listings-in-kuala-lumpur) | KL Property Listings            | ~52,000 | Public              |
| [Kaggle](https://www.kaggle.com/)                                                      | Malaysia House Price Data 2025  | ~3,000  | Public              |
| [data.gov.my / DOSM](https://data.gov.my/)                                             | Household income by state       | 303     | CC BY 4.0           |
| [GADM](https://gadm.org/)                                                              | Malaysia state boundary GeoJSON | —       | Free non-commercial |

---

## 🔌 API Reference

All endpoints are on Laravel (port 8000). Python endpoints are internal.

### Properties

```
GET  /api/properties                  Paginated listing with filters
GET  /api/properties/{id}             Single property
GET  /api/properties/{id}/similar     Similar listings
GET  /api/properties/stats/summary    KPI cards
```

**Filter params:** `state`, `city`, `property_type`, `tenure`, `bedrooms`, `min_price`, `max_price`, `sort_by`, `sort_dir`, `page`

### Analytics (proxied to Python)

```
POST /api/analytics/predict           ML price prediction
GET  /api/analytics/trends/{state}    Plotly price trend chart
GET  /api/analytics/distribution      Plotly price histogram
GET  /api/analytics/psf-by-state      Plotly PSF box plot
GET  /api/analytics/type-breakdown    Plotly property type pie
GET  /api/analytics/affordability-bar Plotly affordability bar
GET  /api/analytics/affordability     Affordability index by state
GET  /api/analytics/correlation       Pearson correlation matrix
GET  /api/analytics/demographic       DOSM cross-analysis
GET  /api/analytics/map/choropleth    State analytics for Leaflet
GET  /api/analytics/map/heatmap       Listing density points
```

---

## 🗃️ Database Schema

```sql
-- properties (from Kaggle CSV)
id, title, state, city, area, property_type, tenure,
price DECIMAL(15,2), price_per_sqft, size_sqft DECIMAL(10,2),
bedrooms, bathrooms, car_parks, furnishing,
lat, lng, listed_at, created_at, updated_at

-- dosm_demographics (from data.gov.my)
id, state, district, year, population,
median_household_income, mean_household_income,
unemployment_rate, urbanisation_rate, population_density,
created_at, updated_at

-- prediction_logs
id, input_features JSONB, predicted_price, model_version, created_at
```

---

## 🚀 Local Development

### Prerequisites

- PHP 8.4 + Composer
- Node.js 20+
- Python 3.11+ + pip
- MySQL 8 (local) or PostgreSQL 16 (production)

### Setup

**1. Clone**

```bash
git clone https://github.com/naufalkhir/malaysia-property-dashboard.git
cd malaysia-property-dashboard
```

**2. Laravel API**

```bash
cd laravel-api
composer install
cp .env.example .env
php artisan key:generate
# Edit .env: DB_CONNECTION=mysql, DB credentials, PYTHON_SERVICE_URL=http://127.0.0.1:8001
php artisan migrate
php artisan serve
```

**3. Python Service**

```bash
cd python-service
python -m venv venv
source venv/Scripts/activate   # Windows
# source venv/bin/activate      # Mac/Linux
pip install -r requirements.txt
cp .env.example .env
# Edit .env: DB_DRIVER=mysql, DB credentials
python train_model.py          # generates price_model.pkl (~176MB, gitignored)
uvicorn main:app --reload --port 8001
```

**4. Nuxt Frontend**

```bash
cd nuxt-frontend
npm install
# Create .env:
echo "NUXT_PUBLIC_API_BASE=http://localhost:8000" > .env
npm run dev
```

**5. Import data via Tinker**

```bash
cd laravel-api
php artisan tinker
# Paste import scripts from DATA_IMPORT_GUIDE.md
```

---

## 🐳 Docker (Production)

```bash
# Build and start all 4 containers
docker compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker compose -f docker-compose.prod.yml exec laravel-api php artisan migrate

# Copy and run ML model (model is gitignored — copy from local or train on server)
scp python-service/price_model.pkl root@YOUR_VPS:/tmp/price_model.pkl
docker compose -f docker-compose.prod.yml cp /tmp/price_model.pkl python-service:/app/price_model.pkl
docker compose -f docker-compose.prod.yml restart python-service

# Check all containers
docker compose -f docker-compose.prod.yml ps
```

---

## ⚙️ DevOps

| Component     | Choice                            | Reason                                            |
| ------------- | --------------------------------- | ------------------------------------------------- |
| VPS           | Hostinger KVM 2 (2 vCPU, 8GB RAM) | Affordable, full root access                      |
| Reverse proxy | Nginx host-level                  | SSL termination before Docker                     |
| SSL           | Let's Encrypt + Certbot           | Free, auto-renews                                 |
| CI/CD         | GitHub Actions                    | 3 workflows: deploy, PR checks, nightly DB backup |
| Containers    | Docker + Compose                  | Dev/prod parity                                   |

---

## 🗂️ Project Structure

```
malaysia-realty-analyzer/
├── .github/workflows/          CI/CD pipelines (deploy, pr-checks, backup)
├── laravel-api/                Laravel 12 REST API
│   ├── app/Http/Controllers/   PropertyController, AnalyticsController, ImportController
│   ├── app/Models/             Property model with query scopes
│   ├── app/Services/           PythonAnalyticsService (HTTP client)
│   └── database/migrations/    properties, dosm_demographics, prediction_logs
├── python-service/             FastAPI microservice
│   ├── routers/                predictions, charts, stats, geodata, etl
│   ├── services/db.py          SQLAlchemy + query_df() helper
│   └── train_model.py          Random Forest training (R²=0.836)
├── nuxt-frontend/              Nuxt 3 frontend
│   └── app/pages/              listings/ (SSR), dashboard/ (CSR)
├── nginx/realty.conf           Rate limiting + security headers + gzip
├── docker-compose.yml          Development (hot reload)
└── docker-compose.prod.yml     Production (internal networks, healthchecks)
```

---

## 🛠️ Key Technical Decisions

**Why proxy Python through Laravel?**
Security. Python has no authentication. Routing through Laravel keeps Python on a private Docker network with rate limiting applied at the Nginx level.

**Why PostgreSQL on production but MySQL locally?**
MySQL was already running locally via Laragon. PostgreSQL was chosen for production due to better analytics support (window functions, JSONB, percentile queries).

**Why Leaflet instead of Google Maps?**
Zero cost, no API key, no rate limits. GADM GeoJSON boundaries + OpenStreetMap tiles provide everything needed.

**Why is the ML model gitignored?**
At 176MB, the `.pkl` file is too large for GitHub. It's regenerated by running `train_model.py` or copied manually to the VPS.

---

## 📝 License

MIT — free to use as a reference for your own portfolio projects.

---

_Built with Laravel, Nuxt, FastAPI, PostgreSQL, Docker, and a lot of `php artisan tinker`._
