import { defineConfig } from 'vite'
import { resolve } from 'path'
import Vue from '@vitejs/plugin-vue'


export default defineConfig(({ mode }) => {
    return {
        plugins: [Vue()],
        base: mode === 'production' ? '/static/dist/' : '/static/', // 🔥 Ajusta en producción
        build: {
            manifest: true,
            emptyOutDir: true,
            outDir: resolve('./dist'),
            rollupOptions: {
                input: {
                    tailwind: resolve('./src/style.css'),
                },
            },
        },
        server: {
            host: '0.0.0.0',
            port: 5173,
            strictPort: true,
            cors: true,
        },
    };
});
