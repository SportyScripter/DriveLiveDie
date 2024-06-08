import { configDefaults, defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 5173,
    host: "127.0.0.1",
  },
  plugins: [react()],
  test: {
    exclude: [...configDefaults.exclude, "src/App.tsx", "src/main.tsx"],
    environment: "jsdom",
    globals: true,
    coverage: {
      exclude: [
        "src/main.tsx",
        "src/App.tsx",
        "src/postcss.config.js",
        "src/tailwind.config.js",
        "src/.eslintrc.cjs",
      ],
    },
  },
});
