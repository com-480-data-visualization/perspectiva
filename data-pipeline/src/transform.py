from datetime import date

import polars as pl

from src.domains import TLD_TO_ISO3, DOMAIN_TO_ISO3, TLD_GENERIC


def _domain_to_country(domain: str) -> str | None:
    """Map a SourceCommonName domain to an ISO3 country code, or None if unmappable."""
    if not domain:
        return None
    domain = domain.strip().lower()
    tld = domain.split(".")[-1]

    # Step 1: country-code TLD (.fr, .de, .ua, ...)
    if tld not in TLD_GENERIC and tld in TLD_TO_ISO3:
        return TLD_TO_ISO3[tld]

    # Step 2: curated domain list
    if domain in DOMAIN_TO_ISO3:
        return DOMAIN_TO_ISO3[domain]

    # Step 3: drop — aggregator or unknown source
    return None


def transform(df: pl.DataFrame) -> pl.DataFrame:
    """
    Takes raw GDELT GKG rows and returns aggregated sentiment by source country + date.
    Output schema: date (Date), country_iso3 (Utf8), avg_tone (Float64), article_count (UInt32)
    """
    print("Transforming data...")

    # 1. Parse DATE int (YYYYMMDDHHMMSS) → Date
    df = df.with_columns(
        pl.col("DATE")
        .cast(pl.Utf8)
        .str.slice(0, 8)
        .str.to_date("%Y%m%d")
        .alias("date")
    )

    # 2. Extract AvgTone — first value in the comma-separated V2Tone string
    df = df.with_columns(
        pl.col("V2Tone")
        .str.split(",")
        .list.first()
        .cast(pl.Float64)
        .alias("tone")
    )

    # 3. Map source domain → ISO3 country (only keep mappable domains)
    domain_map: dict[str, str] = {
        d: country
        for d in df["SourceCommonName"].drop_nulls().unique().to_list()
        if (country := _domain_to_country(d)) is not None
    }
    df = df.with_columns(
        pl.col("SourceCommonName")
        .replace(domain_map)
        .alias("country_iso3")
    )

    # 4. Drop rows with no country (aggregators, unknown sources)
    df = df.filter(
        pl.col("country_iso3").is_not_null() &
        pl.col("country_iso3").str.len_chars().eq(3)
    )

    # 5. Aggregate by source country + date
    agg = (
        df.group_by(["date", "country_iso3"])
        .agg([
            pl.col("tone").mean().alias("avg_tone"),
            pl.col("DocumentIdentifier").n_unique().alias("article_count"),
        ])
        .sort(["date", "country_iso3"])
    )

    # 6. Forward-fill gaps: every country gets a row for every day in the range.
    #    article_count = 0 on silent days, avg_tone = last known value.
    date_min: date = agg["date"].min()  # type: ignore[assignment]
    date_max: date = agg["date"].max()  # type: ignore[assignment]
    all_dates = pl.date_range(date_min, date_max, interval="1d", eager=True).alias("date")
    all_countries = agg["country_iso3"].unique()

    spine = all_dates.to_frame().join(all_countries.to_frame(), how="cross")
    filled = (
        spine
        .join(agg, on=["date", "country_iso3"], how="left")
        .sort(["country_iso3", "date"])
        .with_columns([
            pl.col("avg_tone").forward_fill().over("country_iso3"),
            pl.col("article_count").fill_null(0),
        ])
    )

    print(f"  Date range : {filled['date'].min()} → {filled['date'].max()}")
    print(f"  Countries  : {filled['country_iso3'].n_unique()}")
    print(f"  Total rows : {len(filled):,}")

    return filled
