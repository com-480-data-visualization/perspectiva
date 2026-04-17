'use client';

import type { AnalysisMode } from './WorldMap';

export default function Legend({ mode }: { mode: AnalysisMode }) {
  if (mode === 'sentiment') {
    return (
      <div className="flex items-center gap-2 text-xs text-stone-600">
        <span className="font-medium text-green-700">positive</span>
        <div
          className="h-3 w-36 rounded-sm"
          style={{
            background:
              'linear-gradient(to right, rgb(60,150,80), rgb(221,217,208), rgb(160,30,30))',
          }}
        />
        <span className="font-medium text-red-700">negative</span>
        <button className="ml-1 text-stone-400 hover:text-stone-600" title="How we measure sentiment">
          ⓘ
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 text-xs text-stone-600">
      <span className="font-medium">less</span>
      <div
        className="h-3 w-36 rounded-sm"
        style={{
          background: 'linear-gradient(to right, #ddd9d0, #C97432)',
        }}
      />
      <span className="font-medium">more</span>
      <button className="ml-1 text-stone-400 hover:text-stone-600" title="Total articles from that country">
        ⓘ
      </button>
    </div>
  );
}
