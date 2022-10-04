module.exports = {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        blue: {
          50: "#EFF6FF",
          100: "#D3E1FF",
          200: "#A8C1FF",
          300: "#7DA0FF",
          400: "#5D84FF",
          500: "#2757FF",
          600: "#1C42DB",
          700: "#1330B7",
          800: "#0C2193",
          900: "#07167A",
        }
      },
      borderColor: (theme) => ({
        DEFAULT: theme('colors.gray.300', 'currentColor')
      }),
    }
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
