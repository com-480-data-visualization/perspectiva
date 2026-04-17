import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',          // static HTML/JS — no Node server needed
  basePath: '/perspectiva',  // GitHub Pages serves at /perspectiva
  trailingSlash: true,       // required for GH Pages file routing
  images: { unoptimized: true }, // next/image doesn't work in static export
  env: {
    NEXT_PUBLIC_BASE_PATH: '/perspectiva',
  },
};

export default nextConfig;
