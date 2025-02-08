import { defineConfig } from 'vite'
import { resolve } from 'path'
import Vue from '@vitejs/plugin-vue'


export default defineConfig((mode) => {
    return {
        plugins: [Vue()],
        base: '/static/', // Important later!
        build: {
            manifest: true,
            emptyOutDir: true,
            outDir: resolve('./dist'), // Important later!
            rollupOptions: {
                input: {
                    tailwind: resolve('./src/style.css'),
                },
            },
        },
        server:{
            host: '127.0.0.1',
            port: 5173,
            strictPort: true,
            cors: true,
        }
    };
});