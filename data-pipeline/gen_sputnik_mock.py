"""
Generate realistic mock data for Sputnik-V vaccine coverage (Aug 2020 – Dec 2021).

Sentiment ground truth:
  Russia          very positive  (+3 to +5)  — made the vaccine
  Belarus/KAZ     positive       (+1 to +3)  — allied states, early adopters
  ARG/HUN/SRB     mildly positive (0 to +2)  — early procurers
  EU/USA/UKR      negative       (-2 to -4)  — skeptical / didn't approve
  CHN/IND/VNM     near-neutral   (-0.5 to +1) — business pragmatism
  Africa          near-neutral   (-1 to +0.5)
"""
import pyarrow as pa
import pyarrow.parquet as pq
import json, random, datetime, os, math

random.seed(7)

COUNTRIES = {
    # Russia & allies — positive
    "RUS": +3.8, "BLR": +2.4, "KAZ": +1.9, "AZE": +1.2, "ARM": +1.0,
    # Early adopters — mild positive
    "ARG": +1.5, "HUN": +1.1, "SRB": +1.3, "BOL": +0.9, "VEN": +0.8,
    # West — skeptical / negative
    "USA": -3.2, "GBR": -3.0, "DEU": -2.7, "FRA": -2.5, "ITA": -2.1,
    "ESP": -2.2, "NLD": -2.6, "POL": -3.5, "UKR": -4.0, "SWE": -2.8,
    "CHE": -2.3, "AUT": -2.0, "BEL": -2.4, "CZE": -2.9, "DNK": -2.6,
    "NOR": -2.7, "FIN": -2.5, "PRT": -2.1, "GRC": -1.9, "ROU": -2.3,
    "AUS": -2.5, "CAN": -2.9, "ISR": -2.2,
    # Pragmatic — near neutral
    "CHN": +0.4, "IND": +0.6, "BRA": -0.8, "MEX": -0.5, "COL": -0.4,
    "PHL": +0.3, "VNM": +0.5, "IDN": -0.3, "MYS": -0.2, "SGP": -0.7,
    "JPN": -1.5, "KOR": -1.2, "PAK": +0.7, "BGD": +0.4,
    "IRN": +0.8, "TUR": -0.3, "SAU": -0.1, "ARE": +0.2,
    # Africa
    "NGA": -0.3, "ZAF": -0.6, "KEN": -0.4, "EGY": +0.3,
    # LA
    "PER": -0.3, "ECU": -0.2, "CHL": +0.2, "CUB": +1.4,
}

# Key timeline events that shift coverage volume
EVENTS = {
    "2020-08-11": "Russia announces Sputnik V registration",
    "2020-11-11": "Phase 3 results published in The Lancet",
    "2021-02-02": "Lancet efficacy study: 91.6%",
    "2021-02-19": "EU begins evaluation",
    "2021-03-05": "Hungary starts vaccinations (first EU)",
    "2021-04-13": "Argentina, Mexico, India producing locally",
    "2021-06-15": "WHO emergency use listing review",
    "2021-09-01": "UN General Assembly — Russia pushes adoption",
}

start_date = datetime.date(2020, 8, 11)
end_date   = datetime.date(2021, 12, 31)

dates_list, iso3s, tones, counts = [], [], [], []

d = start_date
while d <= end_date:
    d_str = str(d)
    # Volume boost around key events
    event_boost = 1.0
    for ev_date in EVENTS:
        delta = abs((d - datetime.date.fromisoformat(ev_date)).days)
        if delta <= 7:
            event_boost = max(event_boost, 3.0 - delta * 0.25)

    for iso3, base_tone in COUNTRIES.items():
        # ~10% chance of no coverage any given day
        has_coverage = random.random() > 0.10
        if not has_coverage:
            dates_list.append(d); iso3s.append(iso3); tones.append(None); counts.append(0)
            d += datetime.timedelta(0)  # no-op (handled below)
            continue

        # Scale coverage by event proximity and country importance
        importance = {"RUS": 3.0, "USA": 2.5, "GBR": 2.0, "DEU": 1.8,
                      "FRA": 1.6, "CHN": 1.4, "IND": 1.3}.get(iso3, 1.0)
        base_count = int(random.randint(5, 80) * importance * event_boost)
        article_count = max(1, base_count)

        # Slight drift — sentiment softens a bit over time as vaccine normalises
        months_elapsed = (d - start_date).days / 30
        drift = -0.02 * months_elapsed if base_tone < 0 else 0.01 * months_elapsed
        tone = round(base_tone + random.gauss(0, 0.5) + drift, 4)

        dates_list.append(d)
        iso3s.append(iso3)
        tones.append(tone)
        counts.append(article_count)

    d += datetime.timedelta(days=1)

schema = pa.schema([
    pa.field("date", pa.date32()),
    pa.field("country_iso3", pa.string()),
    pa.field("avg_tone", pa.float64()),
    pa.field("article_count", pa.uint32()),
])

table = pa.table({
    "date": pa.array(dates_list, type=pa.date32()),
    "country_iso3": pa.array(iso3s, type=pa.string()),
    "avg_tone": pa.array(tones, type=pa.float64()),
    "article_count": pa.array(counts, type=pa.uint32()),
}, schema=schema)

out_dir = os.path.join(os.path.dirname(__file__), "..", "app", "public", "data")
os.makedirs(out_dir, exist_ok=True)
slug = "sputnik-v-2020-08-2021-12"
parquet_path = os.path.join(out_dir, f"{slug}.parquet")
pq.write_table(table, parquet_path, compression="snappy")
print(f"Parquet: {len(table)} rows → {parquet_path}")

# Export JSON for static serving
by_date: dict = {}
for i in range(len(table)):
    d_str = str(table["date"][i].as_py())
    tone_val = table["avg_tone"][i].as_py()
    count_val = int(table["article_count"][i].as_py())
    if tone_val is not None and not (isinstance(tone_val, float) and math.isnan(tone_val)):
        tone_val = round(float(tone_val), 4)
    else:
        tone_val = None
    by_date.setdefault(d_str, []).append({
        "country_iso3": table["country_iso3"][i].as_py(),
        "avg_tone": tone_val,
        "article_count": count_val,
    })

all_dates = sorted(by_date.keys())
json_path = os.path.join(out_dir, f"{slug}.json")
with open(json_path, "w") as f:
    json.dump({"dates": all_dates, "by_date": by_date, "events": EVENTS}, f, separators=(",", ":"))
print(f"JSON: {len(all_dates)} dates → {json_path}")
