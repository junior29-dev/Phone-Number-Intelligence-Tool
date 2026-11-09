import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: { paper: "#E8EDEF", ink: "#0D1B22", line: "#B9C6CC", signal: "#D4361F" },
      fontFamily: { sans: ["var(--font-sans)", "system-ui", "sans-serif"] },
    },
  },
} satisfies Config;
