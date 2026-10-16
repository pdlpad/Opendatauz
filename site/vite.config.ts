import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// База сайта = имя репозитория: https://pdlpad.github.io/Opendatauz/
// При переименовании репозитория меняется только эта строка.
export default defineConfig({
  base: '/Opendatauz/',
  plugins: [react()],
})
