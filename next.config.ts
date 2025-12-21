import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  // Fix for local Turbopack permission issues (not needed on Vercel)
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;
