"""Convert parquet to a JSON payload served statically by the app."""
import pyarrow.parquet as pq
import json
import os
import math

PARQUET = os.path.join(
    os.path.dirname(__file__), "..", "app", "public", "data",
    "ukraine-war-2022-02-2022-03.parquet"
)
OUT = os.path.join(
    os.path.dirname(__file__), "..", "app", "public", "data",
    "ukraine-war-2022-02-2022-03.json"
)

table = pq.read_table(PARQUET)
df = table.to_pydict()

# Group by date
by_date: dict[str, list] = {}
for i in range(len(df["date"])):
    d = str(df["date"][i])  # already a date object, str() gives YYYY-MM-DD
    iso3 = df["country_iso3"][i]
    tone = df["avg_tone"][i]
    count = int(df["article_count"][i])
    # Skip NaN / None
    if tone is not None and not (isinstance(tone, float) and math.isnan(tone)):
        tone = round(float(tone), 4)
    else:
        tone = None
    by_date.setdefault(d, []).append({
        "country_iso3": iso3,
        "avg_tone": tone,
        "article_count": count,
    })

dates = sorted(by_date.keys())

payload = {
    "dates": dates,
    "by_date": by_date,
}

with open(OUT, "w") as f:
    json.dump(payload, f, separators=(",", ":"))

print(f"Exported {len(dates)} dates, {sum(len(v) for v in by_date.values())} rows → {OUT}")
