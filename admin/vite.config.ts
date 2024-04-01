import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';

// https://vitejs.dev/config/
export default defineConfig({
	server: {
		host: true,
		port: 8080,
	},
	plugins: [
		react(),
		eslint({
			cache: false,
			include: ['./src/**/*.ts', './src/**/*.tsx'],
			exclude: ['./src/shadcn-components/**', './src/lib/**'],
			lintOnStart: true,
		}),
	],
	resolve: {
		alias: [{ find: '@', replacement: '/src' }],
	},
});
