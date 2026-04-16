"""
Quick EDA chart for any pipeline output parquet.

Usage:
  python eda.py output/sputnik-vaccine-covid-2020-08-2021-08.parquet
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import polars as pl


TOP_N = 30  # max countries to show


def tone_color(tone: float) -> tuple:
    """Map avg_tone to a colour: dark red (very negative) → yellow (neutral) → dark green (positive)."""
    # clamp to [-5, 2]
    t = max(-5.0, min(2.0, tone))
    if t < 0:
        frac = t / -5.0          # 0 (neutral) → 1 (very negative)
        r = 1.0
        g = 1.0 - frac * 0.85   # yellow → red
        b = 0.0
    else:
        frac = t / 2.0           # 0 (neutral) → 1 (positive)
        r = 1.0 - frac
        g = 0.6 + frac * 0.3
        b = 0.0
    return (r, g, b)


def main(parquet_path: str) -> None:
    path = Path(parquet_path)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    df = pl.read_parquet(path)

    # Only count days where articles actually appeared (not forward-filled)
    active = df.filter(pl.col("article_count") > 0)

    # Aggregate per country
    by_country = (
        active
        .group_by("country_iso3")
        .agg([
            pl.col("article_count").sum().alias("total_articles"),
            (
                (pl.col("avg_tone") * pl.col("article_count")).sum()
                / pl.col("article_count").sum()
            ).alias("mean_tone"),
        ])
        .sort("total_articles", descending=True)
        .head(TOP_N)
    )

    countries   = by_country["country_iso3"].to_list()
    totals      = by_country["total_articles"].to_list()
    tones       = by_country["mean_tone"].to_list()

    grand_total = sum(totals)
    pct         = [100 * t / grand_total for t in totals]
    colors      = [tone_color(t) for t in tones]

    n = len(countries)

    # Derive title parts from filename
    stem   = path.stem                       # e.g. sputnik-vaccine-covid-2020-08-2021-08
    parts  = stem.rsplit("-", 2)
    topic  = parts[0].replace("-", " ").title() if len(parts) == 3 else stem
    period = f"{parts[1]} to {parts[2]}" if len(parts) == 3 else ""

    date_min = df["date"].min()
    date_max = df["date"].max()
    n_countries = df["country_iso3"].n_unique()
    total_articles_all = int(df["article_count"].sum())

    fig, (ax_vol, ax_tone) = plt.subplots(
        1, 2,
        figsize=(16, max(6, n * 0.38 + 2)),
        sharey=True,
    )
    fig.suptitle(
        f"{topic} Coverage — {date_min} to {date_max}\n"
        f"{n_countries} source countries · {total_articles_all:,} total articles",
        fontsize=13,
        fontweight="bold",
        y=1.01,
    )

    y = list(range(n - 1, -1, -1))  # top country at top

    # — Left: % of total articles —
    ax_vol.barh(y, [pct[i] for i in range(n)], color=colors, edgecolor="white", linewidth=0.4)
    ax_vol.set_yticks(y)
    ax_vol.set_yticklabels(countries, fontsize=8)
    ax_vol.set_xlabel("% of total articles", fontsize=9)
    ax_vol.set_title("Coverage share by source country", fontsize=10)
    ax_vol.xaxis.set_tick_params(labelsize=8)
    for i, (yi, p) in enumerate(zip(y, pct)):
        ax_vol.text(p + 0.1, yi, f"{p:.1f}%", va="center", fontsize=7, color="#444")

    # — Right: mean sentiment —
    ax_tone.barh(y, [tones[i] for i in range(n)], color=colors, edgecolor="white", linewidth=0.4)
    ax_tone.set_xlabel("Mean tone  (more negative ←)", fontsize=9)
    ax_tone.set_title("Mean sentiment by source country", fontsize=10)
    ax_tone.xaxis.set_tick_params(labelsize=8)
    ax_tone.axvline(0, color="#888", linewidth=0.7, linestyle="--")

    plt.tight_layout()

    out = path.parent / f"eda_{path.stem}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved → {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eda.py <path-to-parquet>")
        sys.exit(1)
    main(sys.argv[1])
