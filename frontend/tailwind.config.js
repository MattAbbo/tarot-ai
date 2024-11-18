/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        purple: {
          400: '#9f7aea',
          500: '#805ad5',
          600: '#6b46c1',
          700: '#553c9a',
        },
        gray: {
          800: '#1a202c',
          900: '#171923',
        },
      },
    },
  },
  plugins: [],
}
