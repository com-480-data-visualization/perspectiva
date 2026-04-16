export type SentimentRow = {
  country_iso3: string; // ISO 3166-1 alpha-3, e.g. "GBR"
  avg_tone: number | null; // mean sentiment; null when article_count = 0 and no prior data to forward-fill
  article_count: number; // 0 = silent/forward-filled day
};

export type SentimentResponse = {
  date: string;               // "YYYY-MM-DD"
  countries: SentimentRow[];
};

export type DatesResponse = {
  dates: string[]; // sorted "YYYY-MM-DD" strings
};
