'use client';

interface DateSliderProps {
  dates: string[];
  currentDate: string;
  onChange: (date: string) => void;
  isPlaying: boolean;
  onPlayPause: () => void;
}

export default function DateSlider({
  dates,
  currentDate,
  onChange,
  isPlaying,
  onPlayPause,
}: DateSliderProps) {
  const currentIndex = dates.indexOf(currentDate);

  function handleSlider(e: React.ChangeEvent<HTMLInputElement>) {
    const idx = Number(e.target.value);
    onChange(dates[idx]);
  }

  function formatDate(d: string) {
    return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  }

  return (
    <div className="flex flex-col gap-2">
      {/* Date label */}
      <div className="text-center text-white font-semibold text-lg tracking-wide">
        {currentDate ? formatDate(currentDate) : '—'}
      </div>

      {/* Controls row */}
      <div className="flex items-center gap-3">
        {/* Play / Pause */}
        <button
          onClick={onPlayPause}
          className="w-8 h-8 flex items-center justify-center rounded-full bg-white/20 hover:bg-white/40 transition-colors text-white text-sm shrink-0"
          aria-label={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? '⏸' : '▶'}
        </button>

        {/* Slider */}
        <input
          type="range"
          min={0}
          max={dates.length - 1}
          value={currentIndex >= 0 ? currentIndex : 0}
          onChange={handleSlider}
          className="flex-1 accent-emerald-400 cursor-pointer"
        />
      </div>

      {/* Start / end labels */}
      <div className="flex justify-between text-xs text-white/60 px-11">
        <span>{dates[0] ? formatDate(dates[0]) : ''}</span>
        <span>{dates[dates.length - 1] ? formatDate(dates[dates.length - 1]) : ''}</span>
      </div>
    </div>
  );
}
