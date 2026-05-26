import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: process.env.GITHUB_PAGES ? '/context-engineering-arena-v2/' : '/',
  build: {
    outDir: 'dist',
  },
})
