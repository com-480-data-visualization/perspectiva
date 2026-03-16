from src.config import TOPIC
from src.pipeline.fetch import fetch_or_load

df = fetch_or_load(TOPIC)
print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")
print(df.head())
