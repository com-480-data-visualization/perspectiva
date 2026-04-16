import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# BigQuery project — set in .env
GCP_PROJECT_ID: str = os.environ["GCP_PROJECT_ID"]

# Pipeline output — review files here before copying to app/public/data/
OUTPUT_DIR: Path = Path(__file__).parents[1] / "output"
