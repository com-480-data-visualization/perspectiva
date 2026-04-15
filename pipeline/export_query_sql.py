from pathlib import Path

from src.config import TOPIC
from src.pipeline.query import build_query


def main() -> None:
    query = build_query(TOPIC)

    out_dir = Path("data") / "queries"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"{TOPIC['name']}.sql"
    out_file.write_text(query + "\n", encoding="utf-8")

    print(f"Saved SQL to: {out_file.resolve()}")
    print("\n--- SQL START ---\n")
    print(query)
    print("\n--- SQL END ---")


if __name__ == "__main__":
    main()
