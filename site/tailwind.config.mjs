import defaultTheme from 'tailwindcss/defaultTheme';
import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
        mono: ['JetBrains Mono', 'Fira Code', ...defaultTheme.fontFamily.mono],
      },
      colors: {
        accent: {
          50:  '#EEEEF8',
          100: '#DDDDF4',
          200: '#BBBCEC',
          300: '#9999E0',
          400: '#7B7EC8',
          500: '#5B5BD6',
          600: '#4A4AC0',
          700: '#3939A8',
          800: '#2C2C8A',
          900: '#1E1E6E',
        },
      },
      maxWidth: {
        content: '1200px',
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            '--tw-prose-body':           'var(--color-text)',
            '--tw-prose-headings':       'var(--color-text)',
            '--tw-prose-lead':           'var(--color-text-2)',
            '--tw-prose-links':          'var(--color-accent)',
            '--tw-prose-bold':           'var(--color-text)',
            '--tw-prose-counters':       'var(--color-text-2)',
            '--tw-prose-bullets':        'var(--color-border-2)',
            '--tw-prose-hr':             'var(--color-border)',
            '--tw-prose-quotes':         'var(--color-text-2)',
            '--tw-prose-quote-borders':  'var(--color-border-2)',
            '--tw-prose-captions':       'var(--color-text-3)',
            '--tw-prose-code':           'var(--color-accent)',
            '--tw-prose-pre-code':       'var(--color-text)',
            '--tw-prose-pre-bg':         'var(--color-surface)',
            '--tw-prose-th-borders':     'var(--color-border-2)',
            '--tw-prose-td-borders':     'var(--color-border)',
            maxWidth: 'none',
            code: {
              backgroundColor: 'var(--color-surface-2)',
              border: '1px solid var(--color-border)',
              borderRadius: '4px',
              padding: '0.15em 0.4em',
              fontWeight: '400',
              '&::before': { content: 'none' },
              '&::after':  { content: 'none' },
            },
            pre: {
              border: '1px solid var(--color-border)',
              borderRadius: '8px',
            },
          },
        },
      }),
    },
  },
  plugins: [
    typography,
  ],
};
