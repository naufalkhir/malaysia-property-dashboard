import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Build MySQL connection string
# Format: mysql+pymysql://user:password@host:port/database
DB_URL = (
    f"mysql+pymysql://"
    f"{os.getenv('DB_USER', 'root')}:"
    f"{os.getenv('DB_PASSWORD', '')}@"
    f"{os.getenv('DB_HOST', '127.0.0.1')}:"
    f"{os.getenv('DB_PORT', '3306')}/"
    f"{os.getenv('DB_NAME', 'malaysia_realty')}"
)

# Engine is the connection pool — reused across all requests
engine = create_engine(DB_URL)


def query_df(sql: str) -> pd.DataFrame:
    """
    Run a SQL query and return results as a pandas DataFrame.
    DataFrame = like a spreadsheet in Python — rows and columns.
    We use this everywhere to manipulate data before sending to frontend.
    """
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)
