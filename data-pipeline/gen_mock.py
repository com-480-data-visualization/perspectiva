"""Generate mock parquet data matching the pipeline schema for local dev."""
import pyarrow as pa
import pyarrow.parquet as pq
import random
import datetime
import os

random.seed(42)

# Countries with approximate sentiment bias for Ukraine war coverage
COUNTRIES = {
    "USA": -2.5, "GBR": -2.8, "DEU": -2.6, "FRA": -2.4, "POL": -3.5,
    "UKR": -4.5, "RUS": 1.2, "BLR": 0.8, "CHN": 0.3, "IND": -0.8,
    "AUS": -2.3, "CAN": -2.7, "JPN": -2.1, "KOR": -1.9, "BRA": -1.2,
    "ARG": -1.4, "ZAF": -1.0, "NGA": -0.9, "ISR": -1.8, "TUR": -0.5,
    "ITA": -2.2, "ESP": -2.1, "NLD": -2.5, "BEL": -2.3, "SWE": -2.6,
    "NOR": -2.7, "DNK": -2.5, "FIN": -2.9, "CHE": -2.0, "AUT": -2.1,
    "CZE": -2.8, "HUN": -1.5, "SVK": -2.4, "ROU": -2.6, "BGR": -1.8,
    "GRC": -1.7, "PRT": -2.0, "MEX": -1.1, "COL": -0.9, "PER": -0.8,
    "PAK": -0.4, "IRN": 0.6, "SAU": -0.3, "ARE": -0.2, "QAT": -0.1,
    "SGP": -1.5, "MYS": -0.7, "IDN": -0.5, "PHL": -1.0, "VNM": -0.3,
    "EGY": -0.5, "KEN": -0.8,
}

ISO3_LIST = list(COUNTRIES.keys())

start_date = datetime.date(2022, 2, 24)
end_date = datetime.date(2022, 3, 24)

dates, iso3s, tones, counts = [], [], [], []

d = start_date
while d <= end_date:
    for iso3, base_tone in COUNTRIES.items():
        # Randomly drop ~15% of entries to simulate sparse coverage
        has_coverage = random.random() > 0.15
        article_count = random.randint(3, 120) if has_coverage else 0
        avg_tone = None
        if has_coverage:
            noise = random.gauss(0, 0.6)
            # Gradually shift sentiment slightly more negative in early March
            day_offset = (d - start_date).days
            drift = -0.05 * (day_offset / 10)
            avg_tone = round(base_tone + noise + drift, 4)

        dates.append(d)
        iso3s.append(iso3)
        tones.append(avg_tone)
        counts.append(article_count)
    d += datetime.timedelta(days=1)

schema = pa.schema([
    pa.field("date", pa.date32()),
    pa.field("country_iso3", pa.string()),
    pa.field("avg_tone", pa.float64()),
    pa.field("article_count", pa.uint32()),
])

table = pa.table(
    {
        "date": pa.array(dates, type=pa.date32()),
        "country_iso3": pa.array(iso3s, type=pa.string()),
        "avg_tone": pa.array(tones, type=pa.float64()),
        "article_count": pa.array(counts, type=pa.uint32()),
    },
    schema=schema,
)

out_dir = os.path.join(os.path.dirname(__file__), "..", "app", "public", "data")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "ukraine-war-2022-02-2022-03.parquet")
pq.write_table(table, out_path, compression="snappy")
print(f"Written {len(table)} rows to {out_path}")
