import { defineConfig } from 'vite'
import { resolve } from 'path'
import Vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
    return {
        plugins: [Vue()],
        base: "/static/",  // Django servirá los archivos desde aquí
        build: {
            manifest: true,
            emptyOutDir: true,
            outDir: resolve('../static/dist'), // Guardar en la carpeta correcta
            rollupOptions: {
                input: resolve('./src/main.js'), // Archivo principal de entrada
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
