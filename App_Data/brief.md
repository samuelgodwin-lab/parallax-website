# Budget Tracker — Claude Code Brief

## Overview

A lightweight, personal budget tracker web app. Built for a single user. No feature bloat — just fast, frictionless expense tracking with voice as the primary input method.

This app uses the **Parallax brand system** — see Section 9 for full design tokens.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | Next.js (App Router) + TypeScript |
| Database & Auth | Supabase (Postgres + Supabase Auth) |
| Hosting | Vercel |
| Charts | Recharts |
| Voice | Web Speech API (browser-native, no API key) |
| App Store (later) | Capacitor (do not set up yet) |

---

## Auth

- Supabase Auth from day one
- Email + password login (keep it simple, no social OAuth for now)
- Single user — no multi-user, no sharing, no roles
- Protect all routes behind auth middleware

---

## Currency & Locale

- Default: INR (₹)
- Support switching currency per transaction (user travels)
- Format numbers in Indian style: ₹1,00,000 not ₹100,000
- Date format: DD/MM/YYYY

---

## Default Categories

Fixed for v1 (no custom categories yet):

- 🍽 Food
- 🚗 Transport
- 🧾 Bills
- 🛍 Shopping
- 🎬 Entertainment
- 📦 Other

---

## Core Features

### 1. Voice Entry (primary — most important)

- Mic button on the main screen, always accessible
- Uses the browser Web Speech API (no third-party service, no API key)
- User speaks naturally: *"spent 350 on groceries"* or *"120 Ola"* or *"paid 2000 for electricity bill"*
- Parser must extract:
  - Amount (required)
  - Category (infer from merchant/keyword)
  - Merchant/note (optional)
  - Currency (default INR, detect if user says "dollars" or "USD")
- Show a confirmation card before saving — user can edit any field
- Must handle Indian merchant names: Swiggy, Zomato, Ola, Uber, BigBasket, Blinkit, BMTC, Namma Metro, Amazon, Flipkart, Netflix, Hotstar, etc.
- Amount formats: "350", "350 rupees", "3500 bucks", "20 dollars"

**Merchant → Category map:**
```
Food: Swiggy, Zomato, BigBasket, Blinkit, Dunzo, restaurant, cafe, lunch, dinner, breakfast, groceries, chai
Transport: Ola, Uber, Rapido, BMTC, Namma Metro, metro, bus, petrol, fuel, cab, auto, rickshaw
Bills: electricity, water, internet, phone, rent, recharge, broadband, gas
Shopping: Amazon, Flipkart, Myntra, Meesho, mall, clothes, shoes
Entertainment: Netflix, Hotstar, Spotify, movie, theatre, concert, game
```

---

### 2. Manual Entry (fallback)

- Simple form: Amount, Category (dropdown), Merchant/Note (optional), Date (default today), Currency (default INR)
- Fast — minimal fields, one tap to save

---

### 3. CSV Import

- Upload a CSV bank statement
- Auto-detect columns (date, description, amount, debit/credit)
- Preview table before importing — user confirms
- Map description → category using same merchant map as voice
- Support common Indian bank CSV formats (HDFC, ICICI, SBI, Axis)

---

### 4. Category Budgets

- User sets a monthly budget limit per category (e.g. Food: ₹8,000/month)
- Live progress bar per category showing spent vs limit
- Visual indicator at >80% (warning) and >100% (over limit)
- Budgets reset on the 1st of each month
- Browser push notification at 80% and 100%

---

### 5. Dashboard

One screen with:

- This month's total spent
- Budget vs actual per category (progress bars)
- Recent transactions list (last 10)
- Donut or bar chart — spending by category this month
- Month switcher for past months

---

## Database Schema (Supabase)

```sql
-- transactions
id uuid primary key
user_id uuid references auth.users
amount decimal not null
currency text default 'INR'
category text not null
merchant text
note text
date date not null
created_at timestamptz default now()
source text -- 'voice' | 'manual' | 'csv'

-- budgets
id uuid primary key
user_id uuid references auth.users
category text not null
amount decimal not null
month text not null -- format: 'YYYY-MM'
created_at timestamptz default now()
```

---

## Project Structure

```
budget-tracker/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── signup/
│   ├── (app)/
│   │   ├── dashboard/
│   │   └── add/
│   └── layout.tsx
├── components/
│   ├── VoiceEntry.tsx      ← most important component
│   ├── ManualEntry.tsx
│   ├── TransactionCard.tsx
│   ├── BudgetProgress.tsx
│   └── CSVImport.tsx
├── lib/
│   ├── supabase.ts
│   ├── voiceParser.ts
│   └── csvParser.ts
├── brand/
│   └── BRAND-GUIDELINES.html
├── docs/
│   └── brief.md
└── README.md
```

---

## Environment Variables

```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

---

## Design System — Parallax Brand

Apply the full Parallax brand system throughout. All CSS must use these tokens — never hardcode values.

### Google Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### CSS Custom Properties — paste into globals.css

```css
:root {
  /* Colour */
  --bg:             oklch(1 0 0);
  --surface:        oklch(0.98 0.001 0);
  --surface-raised: oklch(0.96 0.001 0);
  --text:           oklch(0 0 0);
  --text-2:         oklch(0.40 0.005 0);
  --text-3:         oklch(0.55 0.005 0);
  --accent:         oklch(0.60 0.18 249);
  --accent-hi:      oklch(0.70 0.14 249);
  --accent-muted:   oklch(0.60 0.18 249 / 0.14);
  --accent-soft:    oklch(0.60 0.18 249 / 0.06);
  --border:         oklch(0 0 0 / 0.15);
  --border-strong:  oklch(0 0 0 / 0.30);

  /* Semantic */
  --success: #22c55e;
  --danger:  #dc2626;
  --warning: #f59e0b;

  /* Typography */
  --font-d: 'Bricolage Grotesque', system-ui, sans-serif;
  --font-m: 'JetBrains Mono', 'SF Mono', Consolas, monospace;

  /* Spacing */
  --s1:  4px;  --s2:  8px;  --s3: 12px;
  --s4:  16px; --s6:  24px; --s8: 32px;
  --s12: 48px; --s16: 64px; --s24: 96px;

  /* Motion */
  --ease-out:   cubic-bezier(0.23, 1, 0.32, 1);
  --ease-inout: cubic-bezier(0.77, 0, 0.175, 1);

  /* Layout */
  --w-max:     1400px;
  --w-padding: clamp(24px, 5vw, 80px);
}

*, *::before, *::after { box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-d);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  font-synthesis: none;
}
```

### Typography Rules

- **Headings:** Bricolage Grotesque, weight 700–800, letter-spacing -0.042em to -0.052em, left-aligned always
- **Body:** Bricolage Grotesque, weight 400, line-height 1.6–1.75
- **Labels / mono:** JetBrains Mono, 10px, letter-spacing 0.18em, uppercase
- **Accent word in headings:** `<em style="font-style:normal; color:var(--accent)">word</em>`
- Never centre-align headings

### Hard Rules

- **No border-radius** on structural elements, buttons, or cards — sharp corners only
- **No bounce/spring** easing — use `--ease-out` or `--ease-inout` only
- **Never use `--accent`** as a large background fill — only for text, borders, small icons
- **Never hardcode** colours — always go through token system
- Use `clamp()` for fluid type and spacing

### Component Patterns

**Buttons:**
```css
.btn {
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 12px 24px;
  border: 1px solid var(--border-strong);
  background: transparent;
  color: var(--text);
  cursor: pointer;
  transition: background 0.2s var(--ease-out);
}
.btn:hover { background: var(--accent-soft); }
.btn--accent {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
.btn--accent:hover { background: var(--accent-hi); }
```

**Cards:**
```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: var(--s6);
  /* no border-radius */
}
```

**Budget progress bars:**
- Track: `background: var(--border)`
- Fill default: `background: var(--accent)`
- Fill at >80%: `background: var(--warning)`
- Fill at >100%: `background: var(--danger)`

**Mic button (voice — primary CTA):**
- Large circle, `background: var(--accent)`, no border-radius override needed for circles
- JetBrains Mono label below in 10px uppercase: "HOLD TO SPEAK"
- Active state: pulse ring using `--accent-muted`

---

## What NOT to build (v1)

- No social features
- No investment or net worth tracking
- No recurring transactions
- No bank API / Plaid linking
- No custom categories
- No dark mode
- No Capacitor / app store packaging
- No email parsing

---

## Build Order

1. Scaffold Next.js + TypeScript — paste Parallax tokens into `globals.css`, load fonts in `layout.tsx`
2. Set up Supabase client and auth middleware
3. Build `VoiceEntry.tsx` first — this is the core feature
4. Wire up dashboard with dummy data to validate layout
5. Connect Supabase for real data
6. Add manual entry form
7. Add CSV import last
