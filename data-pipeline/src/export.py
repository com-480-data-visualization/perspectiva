import re
from pathlib import Path

import polars as pl


def export(df: pl.DataFrame, topic: str, date_start: str, date_end: str, output_dir: Path) -> Path:
    """Write the aggregated DataFrame to a Parquet file. Returns the output path."""
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    filename = f"{slug}-{date_start}-{date_end}.parquet"
    path = output_dir / filename

    df.write_parquet(path, compression="snappy")
    print(f"Saved → {path}  ({path.stat().st_size / 1024:.1f} KB)")

    return path
