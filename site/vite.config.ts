import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// База сайта = имя репозитория: https://pdlpad.github.io/Opendata/
// В SPEC.md база указана как /OchiqStat/; при переименовании репо меняется только эта строка.
export default defineConfig({
  base: '/Opendata/',
  plugins: [react()],
})
