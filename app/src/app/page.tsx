'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import WorldMap, { type AnalysisMode } from '@/components/WorldMap';
import Timeline from '@/components/Timeline';
import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';
import Legend from '@/components/Legend';
import type { SentimentRow } from '@/types';

const FILE = 'sputnik-v-2020-08-2021-12';
const PLAY_INTERVAL_MS = 800;

interface DataPayload {
  dates: string[];
  by_date: Record<string, SentimentRow[]>;
  events?: Record<string, string>; // date → event label
}

export default function Home() {
  const [payload, setPayload] = useState<DataPayload | null>(null);
  const [dates, setDates] = useState<string[]>([]);
  const [currentDate, setCurrentDate] = useState<string>('');
  const [countries, setCountries] = useState<SentimentRow[]>([]);
  const [mode, setMode] = useState<AnalysisMode>('sentiment');
  const [isPlaying, setIsPlaying] = useState(false);
  const events = payload?.events ?? {};
  const playTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Load static JSON on mount
  useEffect(() => {
    fetch(`/perspectiva/data/${FILE}.json`)
      .then((r) => r.json())
      .then((data: DataPayload) => {
        setPayload(data);
        setDates(data.dates);
        if (data.dates.length > 0) setCurrentDate(data.dates[0]);
      })
      .catch(console.error);
  }, []);

  // Update countries when date changes
  useEffect(() => {
    if (!payload || !currentDate) return;
    setCountries(payload.by_date[currentDate] ?? []);
  }, [payload, currentDate]);

  // Advance one day
  const advanceDate = useCallback(() => {
    setCurrentDate((prev) => {
      const idx = dates.indexOf(prev);
      if (idx < 0 || idx >= dates.length - 1) {
        setIsPlaying(false);
        return prev;
      }
      return dates[idx + 1];
    });
  }, [dates]);

  useEffect(() => {
    if (isPlaying) {
      playTimerRef.current = setInterval(advanceDate, PLAY_INTERVAL_MS);
    } else {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    }
    return () => { if (playTimerRef.current) clearInterval(playTimerRef.current); };
  }, [isPlaying, advanceDate]);

  const currentDateIndex = dates.indexOf(currentDate);

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-stone-100 font-sans">
      {/* Header */}
      <Header
        mode={mode}
        onModeChange={setMode}
        title="Spread of the news overtime"
      />

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left sidebar */}
        <Sidebar
          countries={countries}
          totalDates={dates.length}
          currentDateIndex={currentDateIndex}
        />

        {/* Main map area */}
        <main className="relative flex-1 flex flex-col overflow-hidden bg-[#ede9e1]">
          {/* Map */}
          <div className="flex-1 relative">
            <WorldMap countries={countries} mode={mode} />
          </div>

          {/* Timeline bar */}
          <div className="shrink-0 bg-[#ede9e1]/95 px-8 pb-5 pt-8">
            {dates.length > 0 && (
              <Timeline
                dates={dates}
                currentDate={currentDate}
                onChange={(d) => { setIsPlaying(false); setCurrentDate(d); }}
                isPlaying={isPlaying}
                onPlayPause={() => setIsPlaying((p) => !p)}
                events={events}
              />
            )}
          </div>

          {/* Legend — bottom center */}
          <div className="absolute bottom-16 left-1/2 -translate-x-1/2 bg-white/80 backdrop-blur-sm border border-stone-200 rounded-full px-4 py-1.5 shadow-sm">
            <Legend mode={mode} />
          </div>
        </main>
      </div>

      {/* Loading screen */}
      {!payload && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-stone-100">
          <div className="text-stone-500 text-sm animate-pulse">Loading data…</div>
        </div>
      )}
    </div>
  );
}
