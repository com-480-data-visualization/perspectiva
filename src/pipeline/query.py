def build_query(topic: dict) -> str:
    """
    Build a BigQuery SQL string for the GDELT GKG partitioned table.

    Uses _PARTITIONDATE for partition pruning — critical to avoid scanning
    the full table (~2.2 TB). Without it, a single query can exhaust the
    1 TB/month free quota.
    """
    date_start = topic["date_start"]   # "YYYY-MM-DD"
    date_end = topic["date_end"]       # "YYYY-MM-DD"

    # GDELT DATE is an integer: YYYYMMDDHHMMSS
    date_start_int = int(date_start.replace("-", "") + "000000")
    date_end_int = int(date_end.replace("-", "") + "235959")

    # Build keyword OR conditions against Themes and DocumentIdentifier
    keyword_clauses = []
    for kw in topic["keywords"]:
        kw = kw.lower()
        keyword_clauses.append(
            f"REGEXP_CONTAINS(LOWER(COALESCE(Themes, '')), r'\\b{kw}\\b')"
        )
        keyword_clauses.append(
            f"REGEXP_CONTAINS(LOWER(COALESCE(DocumentIdentifier, '')), r'{kw}')"
        )
    keyword_filter = "\n    OR ".join(keyword_clauses)

    return f"""SELECT
      DATE,
      SourceCommonName,
      DocumentIdentifier,
      V2Locations,
      V2Tone,
      Themes
    FROM `gdelt-bq.gdeltv2.gkg_partitioned`
    WHERE
      _PARTITIONDATE BETWEEN DATE '{date_start}' AND DATE '{date_end}'
      AND DATE BETWEEN {date_start_int} AND {date_end_int}
      AND (
        {keyword_filter}
      )
    LIMIT 200000"""
