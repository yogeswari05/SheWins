/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["'DM Sans'", "system-ui", "sans-serif"],
        display: ["'Outfit'", "system-ui", "sans-serif"],
      },
      colors: {
        elite: { dark: "#1a0a1c", card: "#2d1424", pink: "#e8a0bf", acc: "#c76b98" },
      },
      keyframes: {
        "eh-float": {
          "0%, 100%": { transform: "translate(0, 0) scale(1)" },
          "50%": { transform: "translate(36px, -28px) scale(1.06)" },
        },
      },
      animation: {
        "eh-float": "eh-float 22s ease-in-out infinite",
        "eh-float-slow": "eh-float 34s ease-in-out infinite reverse",
        "eh-float-delay": "eh-float 28s ease-in-out infinite 4s",
      },
    },
  },
  plugins: [],
};
