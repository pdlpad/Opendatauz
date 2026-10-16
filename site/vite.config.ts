import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// База сайта = имя репозитория: https://pdlpad.github.io/Opendatauz/
// В SPEC.md база указана как /OchiqStat/; репозиторий называется Opendatauz, меняется только эта строка.
export default defineConfig({
  base: '/Opendatauz/',
  plugins: [react()],
})
