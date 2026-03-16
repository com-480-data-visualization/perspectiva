import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery

from src.pipeline.query import build_query

load_dotenv()

_DATA_DIR = Path(__file__).parents[2] / "data" / "processed"


def fetch_or_load(topic: dict) -> pd.DataFrame:
    cache_path = _DATA_DIR / f"{topic['name']}.parquet"

    if cache_path.exists():
        print(f"Loading from cache: {cache_path}")
        return pd.read_parquet(cache_path)

    print(f"Querying BigQuery for topic '{topic['name']}'...")
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_path:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    
    project_id = os.environ["GCP_PROJECT_ID"]

    client = bigquery.Client(project=project_id)
    query = build_query(topic)
    df = client.query(query).to_dataframe()

    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache_path, index=False)
    print(f"Saved {len(df):,} rows to {cache_path}")

    return df
