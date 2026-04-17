'use client';

import type { SentimentRow } from '@/types';

const ISO3_TO_NAME: Record<string, string> = {
  USA: 'United States', GBR: 'United Kingdom', RUS: 'Russia', DEU: 'Germany',
  FRA: 'France', IND: 'India', CHN: 'China', BRA: 'Brazil', ARG: 'Argentina',
  AUS: 'Australia', CAN: 'Canada', UKR: 'Ukraine', POL: 'Poland', ITA: 'Italy',
  ESP: 'Spain', MEX: 'Mexico', KOR: 'South Korea', JPN: 'Japan', TUR: 'Turkey',
  ISR: 'Israel', HUN: 'Hungary', SRB: 'Serbia', BLR: 'Belarus', KAZ: 'Kazakhstan',
  NLD: 'Netherlands', BEL: 'Belgium', SWE: 'Sweden', NOR: 'Norway', DNK: 'Denmark',
  FIN: 'Finland', CHE: 'Switzerland', AUT: 'Austria', CZE: 'Czechia', PRT: 'Portugal',
  GRC: 'Greece', ROU: 'Romania', IRN: 'Iran', SAU: 'Saudi Arabia', ARE: 'UAE',
  ZAF: 'South Africa', NGA: 'Nigeria', KEN: 'Kenya', EGY: 'Egypt', BOL: 'Bolivia',
  VEN: 'Venezuela', CUB: 'Cuba', CHL: 'Chile', PER: 'Peru', COL: 'Colombia',
  SGP: 'Singapore', MYS: 'Malaysia', IDN: 'Indonesia', PHL: 'Philippines',
  VNM: 'Vietnam', PAK: 'Pakistan', BGD: 'Bangladesh', AZE: 'Azerbaijan', ARM: 'Armenia',
};

interface SidebarProps {
  countries: SentimentRow[];
  totalDates: number;
  currentDateIndex: number;
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-[10px] text-stone-400 uppercase tracking-widest font-medium">
        {label}
      </span>
      <span className="text-white text-[26px] font-bold leading-none tracking-tight">
        {value}
      </span>
    </div>
  );
}

export default function Sidebar({ countries, totalDates, currentDateIndex }: SidebarProps) {
  const covered = countries.filter((c) => c.article_count > 0);
  const totalArticles = covered.reduce((s, c) => s + c.article_count, 0);
  const leading = [...covered].sort((a, b) => b.article_count - a.article_count)[0];
  const leadingName = leading ? (ISO3_TO_NAME[leading.country_iso3] ?? leading.country_iso3) : '—';
  const daysElapsed = Math.max(1, currentDateIndex + 1);
  const pace = Math.round(totalArticles / daysElapsed);

  return (
    <aside className="w-[280px] shrink-0 bg-stone-900 flex flex-col overflow-hidden">
      {/* Topic */}
      <div className="px-6 pt-7 pb-4">
        <p className="text-stone-400 text-sm">News about</p>
        <h2 className="text-white text-[22px] font-bold leading-tight mt-0.5">
          the Sputnik vaccine
        </h2>
        {/* Search */}
        <div className="mt-3 flex items-center gap-2 border border-stone-700 rounded px-3 py-2">
          <svg className="w-3 h-3 text-stone-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
          </svg>
          <span className="text-stone-500 text-xs">or search for other topics…</span>
        </div>
      </div>

      <div className="h-px bg-stone-800 mx-6" />

      {/* Stats */}
      <div className="px-6 py-6 flex flex-col gap-6">
        <Stat label="Countries reached" value={covered.length} />
        <Stat label="Leading country (per articles)" value={leadingName} />
        <Stat label="Pace (articles per day)" value={pace.toLocaleString()} />
        <Stat label="Total amount of articles" value={totalArticles.toLocaleString()} />
      </div>

      <div className="h-px bg-stone-800 mx-6" />

      {/* Route mini-viz */}
      <div className="px-6 pt-4 pb-1">
        <span className="text-[10px] text-stone-400 uppercase tracking-widest font-medium">Route</span>
      </div>
      <div className="px-6 pb-4">
        <svg width="100%" height="70" viewBox="0 0 220 70">
          {covered.slice(0, 14).map((c, i) => {
            const cols = 7;
            const x = 14 + (i % cols) * 28;
            const y = 14 + Math.floor(i / cols) * 32;
            const nx = 14 + ((i + 1) % cols) * 28;
            const ny = 14 + Math.floor((i + 1) / cols) * 32;
            return (
              <g key={c.country_iso3}>
                <line x1={x} y1={y} x2={nx} y2={ny} stroke="#C97432" strokeWidth="0.7" opacity="0.6" />
                <circle cx={x} cy={y} r={i === 0 ? 3.5 : 2}
                  fill={i === 0 ? '#4ade80' : '#C97432'} opacity={i === 0 ? 1 : 0.75} />
              </g>
            );
          })}
        </svg>
      </div>

      <div className="flex-1" />

      {/* CTA */}
      <div className="px-6 pb-6 flex flex-col items-center gap-1 text-stone-500">
        <span className="italic text-sm">what else?</span>
        <svg width="12" height="7" viewBox="0 0 12 7" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
          <path d="M1 1l5 5 5-5" />
        </svg>
      </div>
    </aside>
  );
}
