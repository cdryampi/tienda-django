/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "../templates/**/*.html",
    "../**/templates/**/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}