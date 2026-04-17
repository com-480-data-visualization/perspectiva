'use client';

import { Map, Source, Layer } from 'react-map-gl/maplibre';
import type { FillLayerSpecification, LineLayerSpecification, ExpressionSpecification } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import type { SentimentRow } from '@/types';

// Minimal blank map style — no tiles, just a dark ocean background
const BLANK_STYLE = {
  version: 8 as const,
  sources: {},
  projection: { type: 'mercator' },
  layers: [
    {
      id: 'background',
      type: 'background' as const,
      paint: { 'background-color': '#0f172a' },
    },
  ],
};

function toneToColor(tone: number | null): string {
  if (tone === null) return '#374151'; // grey — no coverage
  // Clamp to [-10, 10]
  const t = Math.max(-10, Math.min(10, tone));
  if (t < 0) {
    // negative: white → red
    const ratio = -t / 10;
    const r = Math.round(249 + ratio * (239 - 249));
    const g = Math.round(250 + ratio * (68 - 250));
    const b = Math.round(251 + ratio * (68 - 251));
    return `rgb(${r},${g},${b})`;
  } else {
    // positive: white → green
    const ratio = t / 10;
    const r = Math.round(249 + ratio * (34 - 249));
    const g = Math.round(250 + ratio * (197 - 250));
    const b = Math.round(251 + ratio * (94 - 251));
    return `rgb(${r},${g},${b})`;
  }
}

function buildFillExpression(countries: SentimentRow[]): ExpressionSpecification {
  // ['match', ['get', 'ADM0_A3'], iso3, color, iso3, color, ..., fallback]
  const pairs: string[] = [];
  for (const row of countries) {
    pairs.push(row.country_iso3, toneToColor(row.avg_tone));
  }
  return ['match', ['get', 'ADM0_A3'], ...pairs, '#1e293b'] as unknown as ExpressionSpecification;
}

interface WorldMapProps {
  countries: SentimentRow[];
}

export default function WorldMap({ countries }: WorldMapProps) {
  const fillExpression = buildFillExpression(countries);

  const fillLayer: FillLayerSpecification = {
    id: 'countries-fill',
    type: 'fill',
    source: 'countries',
    paint: {
      'fill-color': fillExpression,
      'fill-opacity': 0.9,
    },
  };

  const outlineLayer: LineLayerSpecification = {
    id: 'countries-outline',
    type: 'line',
    source: 'countries',
    paint: {
      'line-color': '#0f172a',
      'line-width': 0.5,
    },
  };

  return (
    <Map
      initialViewState={{ longitude: 0, latitude: 20, zoom: 1.5 }}
      style={{ width: '100%', height: '100%' }}
      mapStyle={BLANK_STYLE}
      renderWorldCopies={false}
      dragPan={false}
      dragRotate={false}
      scrollZoom={false}
      doubleClickZoom={false}
      touchZoomRotate={false}
      keyboard={false}
    >
      <Source id="countries" type="geojson" data="/world-110m.geojson">
        <Layer {...fillLayer} />
        <Layer {...outlineLayer} />
      </Source>
    </Map>
  );
}
