/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "../templates/**/*.html",
    "../**/templates/**/*.html",
    "./src/**/*.vue",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}