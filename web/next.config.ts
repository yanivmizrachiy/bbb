import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // PGlite ships a WASM build that must stay external to the server bundle.
  serverExternalPackages: ["@electric-sql/pglite"],
};

export default nextConfig;
