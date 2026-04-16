# Perspectiva — News Sentiment Globe

Interactive world map showing how a news event spreads across countries over time and how each country's media feels about it, using GDELT data.

## Visualization Concept
- User picks a topic (e.g. "Russia-Ukraine war")
- Map shows, day by day, how coverage spreads to different countries
- Color = sentiment (positive/negative tone) of that country's media about the topic
- Timeline has "stops" marking moments when other events shift perception
- The unit of analysis is: **how does country X's media feel about topic Y on day Z**

## Stack
- **App**: Next.js (App Router) + TypeScript + Tailwind + MapLibre GL + react-map-gl
- **Data layer**: DuckDB (Node.js) querying parquet files via API routes
- **Pipeline**: Python + Google BigQuery (GDELT source)

## Folder Structure
```
dataviz-project/
├── app/                    # Next.js web app
│   ├── public/data/        # Parquet files served to the app (copy here when ready)
│   └── src/
│       ├── app/
│       │   └── api/sentiment/route.ts
│       ├── components/
│       ├── hooks/
│       ├── lib/
│       │   ├── db.ts       # DuckDB connection
│       │   └── queries.ts  # SQL queries against parquet
│       └── types/
└── data-pipeline/          # Python pipeline (BigQuery → parquet)
    ├── src/
    │   ├── config.py       # GCP project ID, output dir
    │   ├── fetch.py        # BigQuery query + raw data cache
    │   ├── transform.py    # Parse, map source country, aggregate by country+date
    │   ├── export.py       # Write parquet to output/
    │   └── domains.py      # TLD + curated domain → ISO3 country mapping
    ├── output/             # Pipeline staging area (gitignored)
    │   └── cache/          # Raw BigQuery results cache (gitignored)
    ├── run.py              # CLI entry point
    └── requirements.txt
```

## Data Flow
```
GDELT (BigQuery)
    ↓ data-pipeline/src/fetch.py        — keywords + date range query, cached locally
    ↓ data-pipeline/src/transform.py    — source country via domain mapping, daily aggregation
    ↓ data-pipeline/output/             — staging parquet
    ↓ (manual copy when ready)
    ↓ app/public/data/
    ↓ app/src/lib/db.ts                 — DuckDB reads parquet
    ↓ app/src/lib/queries.ts
    ↓ app/src/app/api/sentiment/route.ts
    ↓ React hooks → Map component
```

## Parquet Schema
Output of the pipeline, consumed by DuckDB:
| Column | Type | Description |
|---|---|---|
| `date` | Date | Day (e.g. 2022-02-24) |
| `country_iso3` | String | ISO 3166-1 alpha-3 (e.g. GBR, DEU, UKR) |
| `avg_tone` | Float64 | Mean sentiment that day. Negative = negative coverage |
| `article_count` | UInt32 | Unique articles from that country. 0 = forward-filled day |

## Getting Started

**App:**
```bash
cd app && npm install && npm run dev
```

**Pipeline:**
```bash
cd data-pipeline
source .venv/bin/activate
# Check query cost first
python run.py --topic "ukraine-war" --keywords "ukraine,russia,kyiv,zelensky,putin" \
              --start 2022-02 --end 2022-03 \
              --credentials dataviz-490213-eb4214bb9d4b.json --dry-run
# Run for real
python run.py --topic "ukraine-war" --keywords "ukraine,russia,kyiv,zelensky,putin" \
              --start 2022-02 --end 2022-03 \
              --credentials dataviz-490213-eb4214bb9d4b.json
# Copy to app when happy with the output
cp output/ukraine-war-2022-02-2022-03.parquet ../app/public/data/
```

## Progress

- [x] Data pipeline — GDELT → parquet (`data-pipeline/`)
- [x] **Step 1** — DuckDB layer: `app/src/lib/db.ts`, `queries.ts`, `types/index.ts`
- [x] **Step 2** — API routes: `GET /api/sentiment?date=&file=` and `GET /api/sentiment/dates?file=`
- [ ] **Step 3** — World map: MapLibre GL + world GeoJSON (`app/public/world-110m.geojson`) + country fill colors
- [ ] **Step 4** — Date slider: `app/src/components/DateSlider.tsx`
- [ ] **Step 5** — Data → map wiring: avg_tone color scale, article_count=0 dimmed grey
- [ ] **Step 6** — Polish: loading states, legend (`Legend.tsx`), full-screen layout

### API endpoints (working)
- `GET /api/sentiment/dates?file=<slug>` → `{ dates: string[] }`
- `GET /api/sentiment?date=YYYY-MM-DD&file=<slug>` → `{ date, countries: [{country_iso3, avg_tone, article_count}] }`
- `avg_tone` is `null` when `article_count === 0` (no coverage, not yet forward-filled)

### Key implementation notes
- DuckDB runs server-side only (API routes). `serverExternalPackages: ['duckdb']` in `next.config.ts` keeps it out of the Turbopack bundle.
- Parquet files live in `app/public/data/`. DuckDB reads them via absolute path with `read_parquet()`.
- Map component must be `"use client"` — MapLibre GL is browser-only.

## Course
EPFL COM-480 Data Visualization — Milestone 2 due 2026-04-17, Milestone 3 due 2026-05-29
