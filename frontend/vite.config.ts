import { dirname, resolve } from "path";
import { fileURLToPath } from "url";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

const __d = dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, __d, "");
  const apiProxy = env.VITE_API_PROXY || "http://127.0.0.1:8000";

  return {
    plugins: [react()],
    resolve: { alias: { "@": resolve(__d, "src") } },
    server: {
      port: 5173,
      proxy: {
        "/api": {
          target: apiProxy,
          changeOrigin: true,
        },
      },
    },
    optimizeDeps: {
      rolldownOptions: {}
    }
  };
});
