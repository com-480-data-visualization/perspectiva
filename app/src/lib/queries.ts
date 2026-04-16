import path from 'path';
import { query } from './db';
import type { SentimentRow } from '@/types';

// Build absolute path to a parquet file in public/data/.
// Escape single quotes so the path is safe inside a SQL string literal.
function parquetPath(file: string): string {
  const abs = path.join(process.cwd(), 'public', 'data', `${file}.parquet`);
  return abs.replace(/'/g, "''");
}

/**
 * All countries' sentiment for a given date.
 * Returns an empty array if the date is not present in the file.
 */
export async function getSentimentByDate(
  date: string,
  file: string
): Promise<SentimentRow[]> {
  const p = parquetPath(file);
  return query<SentimentRow>(`
    SELECT
      country_iso3,
      avg_tone,
      CAST(article_count AS INTEGER) AS article_count
    FROM read_parquet('${p}')
    WHERE date = '${date}'::DATE
    ORDER BY country_iso3
  `);
}

/**
 * Sorted list of all distinct dates in the parquet file, as "YYYY-MM-DD" strings.
 */
export async function getAvailableDates(file: string): Promise<string[]> {
  const p = parquetPath(file);
  const rows = await query<{ date: string }>(`
    SELECT DISTINCT CAST(date AS VARCHAR) AS date
    FROM read_parquet('${p}')
    ORDER BY date
  `);
  return rows.map((r) => r.date);
}
