import duckdb from 'duckdb';

// One Database for the process lifetime; connections are created per query.
// Using a module-level global (not `let`) so Turbopack HMR doesn't reset it.
const globalDb = global as typeof global & { __duckdb?: duckdb.Database };
if (!globalDb.__duckdb) {
  globalDb.__duckdb = new duckdb.Database(':memory:');
}
const db = globalDb.__duckdb;

// Each query gets its own Connection — safe for concurrent requests.
export function query<T = Record<string, unknown>>(sql: string): Promise<T[]> {
  return new Promise((resolve, reject) => {
    const conn = db.connect();
    conn.all(sql, (err: duckdb.DuckDbError | null, rows: duckdb.RowData[]) => {
      conn.close();
      if (err) reject(err);
      else resolve(rows as T[]);
    });
  });
}
