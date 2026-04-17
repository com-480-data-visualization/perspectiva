'use client';

import type { AnalysisMode } from './WorldMap';

const MODES: { value: AnalysisMode; label: string }[] = [
  { value: 'sentiment', label: 'sentiment' },
  { value: 'amount', label: 'amount' },
];

interface HeaderProps {
  mode: AnalysisMode;
  onModeChange: (m: AnalysisMode) => void;
  title: string;
}

export default function Header({ mode, onModeChange, title }: HeaderProps) {
  return (
    <header className="h-11 bg-white border-b border-stone-200 flex items-center px-5 shrink-0 gap-4">
      {/* Logo — two overlapping circles (Perspectiva icon) */}
      <span className="font-semibold text-sm tracking-tight text-stone-800 flex items-center gap-2">
        <svg width="28" height="14" viewBox="0 0 28 14" fill="none">
          <circle cx="7" cy="7" r="6" fill="none" stroke="#1c1917" strokeWidth="1.8" />
          <circle cx="7" cy="7" r="6" fill="#1c1917" />
          <circle cx="21" cy="7" r="6" fill="none" stroke="#1c1917" strokeWidth="1.8" />
          <circle cx="21" cy="7" r="6" fill="#1c1917" />
        </svg>
        Perspectiva
      </span>

      {/* Center: map title + analysis dropdown */}
      <div className="flex-1 flex justify-center items-center gap-1.5 text-sm text-stone-700">
        <span className="font-medium">{title} &amp;</span>
        <div className="relative">
          <select
            value={mode}
            onChange={(e) => onModeChange(e.target.value as AnalysisMode)}
            className="appearance-none text-orange-600 font-semibold bg-transparent pr-4 cursor-pointer focus:outline-none"
          >
            {MODES.map((m) => (
              <option key={m.value} value={m.value}>
                {m.label}
              </option>
            ))}
          </select>
          <svg
            className="pointer-events-none absolute right-0 top-1/2 -translate-y-1/2 text-orange-600"
            width="10"
            height="6"
            viewBox="0 0 10 6"
            fill="currentColor"
          >
            <path d="M0 0l5 6 5-6z" />
          </svg>
        </div>
      </div>

      {/* Right: About + flag */}
      <div className="flex items-center gap-4 text-sm text-stone-600">
        <button className="hover:text-stone-900 transition-colors">About</button>
        <span title="English">🇬🇧</span>
      </div>
    </header>
  );
}
