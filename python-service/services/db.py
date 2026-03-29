import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
# This is how we keep passwords out of the code
load_dotenv()

# Read database config from environment variables
# We use getenv(key, default) — if the env var doesn't exist, use the default
DRIVER = os.getenv("DB_DRIVER", "mysql")  # "mysql" locally, "postgresql" on VPS
HOST = os.getenv("DB_HOST", "127.0.0.1")  # "postgres" in Docker (container name)
PORT = os.getenv("DB_PORT", "3306")  # 3306 MySQL, 5432 PostgreSQL
NAME = os.getenv("DB_NAME", "malaysia_realty")
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "")

# Build the connection string based on which database we're using
# SQLAlchemy uses different drivers: pymysql for MySQL, psycopg2 for PostgreSQL
# This lets us use the same code in both local (MySQL) and production (PostgreSQL)
if DRIVER == "postgresql":
    DB_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
else:
    DB_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

# create_engine creates a connection pool — reused across all requests
# Much faster than opening a new connection for every API call
engine = create_engine(DB_URL)


def query_df(sql: str) -> pd.DataFrame:
    """
    Run a raw SQL query and return results as a pandas DataFrame.
    DataFrame is like a spreadsheet in Python — rows and columns.
    We use this everywhere to manipulate data before sending to frontend.
    """
    with engine.connect() as conn:
        # text() wraps the SQL string so SQLAlchemy handles it safely
        return pd.read_sql(text(sql), conn)
