import { configDefaults, defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    exclude: [...configDefaults.exclude, "src/app.jsx", "src/index.jsx"],
    environment: "jsdom",
    globals: true,
    coverage: {
      exclude: ["src/index.jsx", "src/app.jsx"],
    },
  },
});
