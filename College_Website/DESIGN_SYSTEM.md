# DESIGN SYSTEM

## Theme
Warm Maharashtra Marathi school website. Keep every new page devotional, welcoming, educational, and consistent with the index page.

## Color Palette
Use this orange, cream, yellow, and brown family on all pages.

- Page cream: `#F5E6CC`
- Soft cream panel: `#FFF8F0`
- Warm peach section: `#F2D7B6`
- Light saffron: `#FACC15`
- Primary orange: `#C96A2B`
- Deep orange hover: `#A0522D`
- Terracotta accent: `#B85C38`
- Dark brown: `#3E2723`
- Main text brown: `#4A2C1A`
- Muted text brown: `#7A5C45`
- Border brown tint: `rgba(139, 69, 19, 0.12)`

Avoid green, blue, purple, black-heavy, or neon color themes unless the page has a very small functional status badge.

## Typography
- Body font: `Hind`, sans-serif.
- Marathi headings: `Tiro Devanagari Marathi`, serif.
- Heading color: `#4A2C1A` or `#C96A2B`.
- Paragraph color: `#7A5C45`.
- Keep line-height generous: `1.7` to `1.9` for Marathi text.

## Layout
- Max content width: `1200px`.
- Container width: `90%`.
- Section padding: `100px 0` on desktop, smaller on mobile.
- Use two-column grids for hero/about sections and responsive cards for repeated content.
- Keep pages clean and spacious, not crowded.

## Navbar
- Fixed top navbar with cream translucent background: `rgba(245, 230, 204, 0.92)`.
- Use blur: `backdrop-filter: blur(12px)`.
- Nav link hover color: `#C96A2B`.
- Mobile uses hamburger menu and warm peach dropdown: `#F2D7B6`.

## Buttons
- Primary: orange background `#C96A2B`, brown text `#4A2C1A`.
- Primary hover: `#A0522D`, small upward movement.
- Secondary: transparent/cream with orange border.
- Border radius: `12px`.
- Use soft orange shadows only on hover or focus.

## Cards
- Background: `rgba(255, 248, 240, 0.65)` to `rgba(255, 248, 240, 0.78)`.
- Border: `1px solid rgba(139, 69, 19, 0.12)`.
- Radius: `18px` to `22px`.
- Hover: lift `-6px` to `-8px`, orange border, soft orange shadow.
- Do not introduce dark blue cards or green highlights.

## Images And Placeholders
- Use rounded corners between `18px` and `25px`.
- Placeholder blocks should use dark brown `#3E2723` with orange or cream text.
- Real images should feel warm and natural; avoid cold filters.

## Animation Style
Animations should be gentle and premium, never distracting.

- Hero text: fade up on page load.
- Hero/about image blocks: slow floating movement.
- Cards/results/sections: reveal on scroll with fade-up.
- Buttons/cards: smooth hover transform.
- Duration: `0.35s` to `0.8s` for UI transitions.
- Long decorative motion: `5s` to `12s`, subtle only.
- Always support reduced motion with `prefers-reduced-motion`.

## Responsive Breakpoints
- Mobile: `600px`
- Tablet: `992px`
- Desktop content max: `1200px`

## Partner Checklist
Before adding a new page, confirm:

- The page uses the same fonts as the index page.
- The background stays cream/peach, not white/blue/green.
- Buttons use orange and brown.
- Cards use soft cream glass styling.
- Motion is fade-up, floating, or hover-lift only.
- Navbar and footer match the index page.
- Marathi headings use the heading font and warm colors.
