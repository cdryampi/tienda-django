import { defineConfig } from 'vite'
import { resolve } from 'path'


export default defineConfig((mode) => {
    return {
        plugins: [],
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
    };
});