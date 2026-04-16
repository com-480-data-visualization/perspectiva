import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // duckdb ships a native .node binary — opt it out of bundling so Node.js require() handles it.
  serverExternalPackages: ['duckdb'],
};

export default nextConfig;
