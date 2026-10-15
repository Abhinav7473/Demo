import { defineConfig } from "vite";

export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 5173,
    // Served behind nginx on :8080; HMR websocket goes through the proxy.
    hmr: { clientPort: 8080 },
  },
});
