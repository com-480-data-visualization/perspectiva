import duckdb from 'duckdb';

// Module-level singleton — one in-memory DB for the lifetime of the server process.
// DuckDB reads parquet files directly via read_parquet(); no data is imported.
let db: duckdb.Database | null = null;

function getDb(): duckdb.Database {
  if (!db) {
    db = new duckdb.Database(':memory:');
  }
  return db;
}

// Uses .stream() which returns an AsyncIterable — no manual Promise wrapping needed.
export async function query<T = Record<string, unknown>>(sql: string): Promise<T[]> {
  const rows: T[] = [];
  for await (const row of getDb().stream(sql)) {
    rows.push(row as T);
  }
  return rows;
}
