## 2026-06-06 - Nav active state: CSS defined but never applied
Learning: This site had `.top-nav a.active { color: var(--accent); }` in the stylesheet from the start, but no page ever set `class="active"` on its own nav link. The ghost rule was invisible until inspected. Pattern to watch for: orphaned CSS active/current selectors that look intentional but were never wired up.
Action: On any multi-page static site, always verify that nav active-state CSS is actually applied via `class="active"` + `aria-current="page"` on each page's own link — not just present in the stylesheet.
