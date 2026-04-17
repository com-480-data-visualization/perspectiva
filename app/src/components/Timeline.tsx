'use client';

interface TimelineProps {
  dates: string[];
  currentDate: string;
  onChange: (date: string) => void;
  isPlaying: boolean;
  onPlayPause: () => void;
  events?: Record<string, string>; // date → label
}

function formatDateLabel(d: string) {
  if (!d) return '';
  const dt = new Date(d + 'T00:00:00');
  return dt
    .toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
    .toLowerCase();
}

export default function Timeline({
  dates,
  currentDate,
  onChange,
  isPlaying,
  onPlayPause,
  events = {},
}: TimelineProps) {
  const currentIndex = Math.max(0, dates.indexOf(currentDate));
  const pct = dates.length > 1 ? (currentIndex / (dates.length - 1)) * 100 : 0;

  // Find event tick positions as %
  const eventTicks = Object.keys(events)
    .map((d) => {
      const idx = dates.indexOf(d);
      if (idx < 0) return null;
      return { pct: (idx / (dates.length - 1)) * 100, label: events[d], date: d };
    })
    .filter(Boolean) as { pct: number; label: string; date: string }[];

  return (
    <div className="flex items-center gap-4 w-full">
      {/* Play / Pause */}
      <button
        onClick={onPlayPause}
        className="w-9 h-9 flex items-center justify-center rounded-full bg-stone-900 hover:bg-stone-700 transition-colors text-white shrink-0 shadow"
        aria-label={isPlaying ? 'Pause' : 'Play'}
      >
        {isPlaying ? (
          <svg width="11" height="13" viewBox="0 0 11 13" fill="currentColor">
            <rect x="0" y="0" width="3.5" height="13" rx="1" />
            <rect x="7.5" y="0" width="3.5" height="13" rx="1" />
          </svg>
        ) : (
          <svg width="12" height="14" viewBox="0 0 12 14" fill="currentColor">
            <path d="M0 0 L12 7 L0 14 Z" />
          </svg>
        )}
      </button>

      {/* Slider track */}
      <div className="relative flex-1 flex items-center" style={{ paddingTop: 28 }}>
        {/* Date bubble */}
        <div
          className="absolute text-xs text-stone-600 bg-white border border-stone-200 rounded px-1.5 py-0.5 shadow-sm pointer-events-none whitespace-nowrap"
          style={{ left: `${pct}%`, top: 0, transform: 'translateX(-50%)' }}
        >
          {formatDateLabel(currentDate)}
        </div>

        {/* Event tick marks above the track */}
        {eventTicks.map((ev) => (
          <div
            key={ev.date}
            className="absolute bottom-5 w-px h-2.5 bg-stone-500 opacity-60 pointer-events-none"
            style={{ left: `${ev.pct}%` }}
            title={ev.label}
          />
        ))}

        {/* Range input */}
        <input
          type="range"
          min={0}
          max={dates.length - 1}
          value={currentIndex}
          onChange={(e) => onChange(dates[Number(e.target.value)])}
          className="w-full h-0.5 appearance-none rounded-full cursor-pointer"
          style={{
            background: `linear-gradient(to right, #1c1917 0%, #1c1917 ${pct}%, #c8c4bc ${pct}%, #c8c4bc 100%)`,
          }}
        />
      </div>
    </div>
  );
}
