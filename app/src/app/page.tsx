import WorldMap from '@/components/WorldMap';
import type { SentimentResponse } from '@/types';

const FILE = 'ukraine-war-2022-02-2022-03';
const DATE = '2022-02-24';

async function getSentiment() {
  const res = await fetch(
    `http://localhost:3000/api/sentiment?date=${DATE}&file=${FILE}`,
    { cache: 'no-store' }
  );
  if (!res.ok) return [];
  const data: SentimentResponse = await res.json();
  return data.countries;
}

export default async function Home() {
  const countries = await getSentiment();

  return (
    <main style={{ width: '100vw', height: '100vh' }}>
      <WorldMap countries={countries} />
    </main>
  );
}
