import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable React strict mode for better error detection
  reactStrictMode: true,
  // Configuration to handle development warnings
  devIndicators: {
    appIsrStatus: true,
  },
  // Ensure proper hydration handling
  experimental: {
    reactCompiler: false, // Disable experimental React compiler that might cause issues
  }
};

export default nextConfig;