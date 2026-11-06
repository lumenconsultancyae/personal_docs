# UX/UI Redesign & Frontend Architectural Upgrade (`feat/ux-style-improvements`)

## 1. Executive Summary

This document records the comprehensive UX/UI redesign, interaction overhaul, and modern frontend architectural upgrade of **Wilson Guevara's Personal Webpage & Engineering Portfolio** (`lumenconsultancyae/personal-webpage` and `lumenconsultancyae/personal_docs`).

### Key Architectural & UX Upgrades

1. **Declarative Routing & Deep-Linkable URL State (`react-router-dom`)**:
   - Replaced the single-page vertical snap-scroll layout (`html, body { overflow: hidden }`) with declarative multi-route navigation (`/`, `/journey`, `/projects`, `/testimonials`, `/personal`, `/contact`) powered by **React Router**, route-level code splitting (`React.lazy` + `<Suspense>`), and backward-compatible hash redirection (`#professionalHighlights`, `#journey`, `#projects`, `#testimonials`, `#aboutme`, `#traveling`, `#philosophy`, `#funfacts`, `#gallery`).
   - Synchronized table pagination (`page`, `pageSize`), debounced search queries (`q`), category/type filters (`category`, `type`, `skillCategory`, `tab`), and sort order (`sort`) with URL search parameters (`useSearchParams`) so every filtered view is bookmarkable and survives full browser reloads.
2. **Server vs. Client State Separation (`@tanstack/react-query`)**:
   - Replaced ad-hoc `useEffect` + `fetch` calls with **TanStack Query v5** (`useQuery`, `useMutation`, `useQueryClient`) backed by deterministic **Query Key Factories** (`src/application/queryKeys.ts`).
   - Implemented **optimistic updates** with automatic rollback on error (`onError`) and targeted cache invalidation on settle (`onSettled`) for projects, peer endorsements, and contact inquiries.
3. **Cohesive Visual Identity, Realm Separation & Semantic CSS Tokens (`src/app/globals.css`)**:
   - Replaced competing cyan/blue vs. neon purple/fuchsia page gradients with a bespoke **Obsidian Carbon, Burnished Copper & Verdigris Teal** semantic token system (`--bg-canvas`, `--bg-surface`, `--bg-elevated`, `--text-primary`, `--text-secondary`, `--accent-primary`, `--accent-secondary`, `--status-success`, `--status-warning`, `--status-danger`, `--status-info`) paired with a **Warm Alabaster & Deep Bronze** light theme (`[data-theme="light"]`), with zero hardcoded hex values inside `.tsx` components.
   - Enforced strict **Professional vs. Personal Realm Separation** (`[data-realm="professional"]` vs. `[data-realm="personal"]`) in `AppShell.tsx` (`PROFESSIONAL_NAV_ITEMS` vs. `PERSONAL_NAV_ITEMS` + dedicated header realm switcher) and kept information density low via progressive disclosure.
   - Enforced `font-variant-numeric: tabular-nums` across KPI metrics, dates, years, pagination counters, and table columns.
   - Adopted CSS logical properties (`margin-inline`, `padding-inline`, `inset-inline`, `text-align: start`) with live **LTR / RTL** switching (`dir="ltr"` / `dir="rtl"`), visual keyboard shortcut badges (`.kbd-hint`), and clean `@media print` stylesheets.
4. **Accessible WAI-ARIA Primitives & Zero Native Browser Dialogs**:
   - **Toast Notification Queue (`src/components/ui/ToastProvider.tsx`)**: Non-blocking `role="status"` / `aria-live="polite"` notifications supporting `success`, `error`, `warning`, and `info` variants, auto-dismiss, manual close, and an **Undo** action callback for reversible deletions.
   - **Accessible Confirmation Modal (`src/components/ui/ConfirmDialog.tsx`)**: Focus-trapped `role="alertdialog"` / `aria-modal="true"` dialog with contextual item summary, `Escape` / backdrop cancellation, and focus restoration.
   - **Schema-First Inline Validation (`react-hook-form` + `zod`)**: Real-time and on-submit validation with field-level `role="alert"` error messages, `aria-invalid="true"`, `aria-describedby`, automatic first-invalid-field focus, and XSS sanitization (`sanitizeText`).
   - **Progressive Disclosure & Command Palette (`Cmd/Ctrl + K`)**: Multi-field creation forms collapse behind primary header CTAs (`+ New Project`, `+ Add Endorsement`), and a `Cmd/Ctrl + K` command palette enables instant route jumping and theme/direction toggling.

---

## 2. Surface / View × State / URL Synchronization Matrix

| Route / Surface | Pathname | Synchronized URL Search Params | Primary TanStack Query Key | Progressive Disclosure / Modal Actions |
| :--- | :--- | :--- | :--- | :--- |
| **Executive Overview** | `/` | — | `["portfolio", "overview"]`, `["portfolio", "projects"]` | Hero CTAs, KPI summary cards, `⌘K` Command Palette |
| **Career & Education** | `/journey` | `type` (`all`\|`work`\|`education`), `q`, `page`, `pageSize` | `["portfolio", "overview"]` | Bounded milestone table + interactive milestone inspector |
| **Projects Explorer** | `/projects` | `q`, `category`, `sort`, `page`, `pageSize`, `create` | `["portfolio", "projects"]` | `+ New Project` / Edit panel (`react-hook-form` + `zod`), Delete `ConfirmDialog` + Undo Toast |
| **Testimonials & Skills** | `/testimonials` | `skillCategory` | `["portfolio", "testimonials"]`, `["portfolio", "overview"]` | `+ Add Endorsement` panel (`react-hook-form` + `zod`), Delete `ConfirmDialog` + Undo Toast |
| **Personal & Gallery** | `/personal` | `tab` (`all`\|`lifestyle`\|`travel`\|`philosophy`\|`funfacts`\|`gallery`) | `["portfolio", "overview"]` | Accessible photo gallery lightbox (`role="dialog"`) |
| **Contact & Inquiries** | `/contact` | — | `["portfolio", "inquiries"]` | Validated Inquiry Form + bounded Inquiries Log table + Delete `ConfirmDialog` + Undo Toast |

---

## 3. Visual Before & After Audit (`docs/screenshots/ux_improvements/`)

### 3.1 Baseline Defects Identified in "Before" Screenshots

| Issue ID | Baseline Defect Observed | Affected Viewport(s) | Before Screenshot Reference | Resolution in `feat/ux-style-improvements` |
| :--- | :--- | :--- | :--- | :--- |
| **UX-01** | Avatar image hand overlaps `"Hi, I am Wilson"` heading text; no top navigation bar or command palette trigger | Desktop (`1440x900`) | `before/home_desktop.png` | Structured 12-column hero grid with dedicated avatar card and sticky `AppShell` header (`after/home_desktop.png`) |
| **UX-02** | `"Professional"` CTA button text overflows and clips on narrow mobile screens (`w-1/3 px-5`) | Mobile (`390x844`) | `before/home_mobile.png` | Fluid flex-wrap CTA buttons and responsive off-canvas navigation drawer (`after/home_mobile.png`, `after/mobile_drawer_open.png`) |
| **UX-03** | Competing visual themes: cyan/blue gradient on Portfolio vs. neon purple/fuchsia gradient on Personal; missing section heading on `#aboutme`; broken emoji glyph `▯` in right nav | Desktop, Tablet, Mobile | `before/portfolio_highlights_desktop.png`, `before/personal_aboutme_desktop.png` | Unified semantic CSS custom properties (`--bg-canvas`, `--bg-surface`, `--accent-primary`) and Lucide SVG icons across all routes (`after/personal_aboutme_desktop.png`) |
| **UX-04** | Unpaginated, clipped project cards with no search, category filter, sort, or page-size selector | Desktop, Tablet, Mobile | `before/portfolio_projects_desktop.png` | Bounded scroll table (`bounded-table-container`) with sticky headers, debounced search (`q`), category/sort selectors, and `PaginationControls` (`after/portfolio_projects_desktop.png`) |
| **UX-05** | No inline form validation, no progressive disclosure creation drawer, and no confirmation modal or Undo toast | Desktop, Tablet, Mobile | `before/portfolio_projects_desktop.png` | Added `ProjectFormPanel`, `TestimonialFormPanel`, `ContactInquiryForm`, `ConfirmDialog`, and `ToastProvider` with Undo (`after/projects_validation_desktop.png`, `after/projects_confirm_delete_desktop.png`) |

### 3.2 Before vs. After Screenshot Catalog

All baseline and post-redesign screenshots are stored under `docs/screenshots/ux_improvements/before/` and `docs/screenshots/ux_improvements/after/`:

- **Executive Overview (`/`)**:
  - Before: `before/home_desktop.png`, `before/home_tablet.png`, `before/home_mobile.png`
  - After: `after/home_desktop.png`, `after/home_tablet.png`, `after/home_mobile.png`
- **Career Journey (`/journey`)**:
  - Before: `before/portfolio_journey_desktop.png`, `before/portfolio_journey_tablet.png`, `before/portfolio_journey_mobile.png`
  - After: `after/portfolio_journey_desktop.png`, `after/portfolio_journey_tablet.png`, `after/portfolio_journey_mobile.png`
- **Projects Explorer (`/projects`)**:
  - Before: `before/portfolio_projects_desktop.png`, `before/portfolio_projects_tablet.png`, `before/portfolio_projects_mobile.png`
  - After: `after/portfolio_projects_desktop.png`, `after/portfolio_projects_tablet.png`, `after/portfolio_projects_mobile.png`
- **Testimonials & Skills (`/testimonials`)**:
  - Before: `before/portfolio_testimonials_desktop.png`, `before/portfolio_testimonials_tablet.png`, `before/portfolio_testimonials_mobile.png`
  - After: `after/portfolio_testimonials_desktop.png`, `after/portfolio_testimonials_tablet.png`, `after/portfolio_testimonials_mobile.png`
- **Personal & Gallery (`/personal`)**:
  - Before: `before/personal_aboutme_desktop.png`, `before/personal_gallery_desktop.png`, `before/personal_aboutme_mobile.png`
  - After: `after/personal_aboutme_desktop.png`, `after/personal_gallery_desktop.png`, `after/personal_aboutme_mobile.png`
- **Interactive States & Accessibility Verification (`after/`)**:
  - `after/command_palette_desktop.png` (`Cmd/Ctrl + K` quick jump modal)
  - `after/projects_validation_desktop.png` (Inline `react-hook-form` + `zod` field-level validation alerts)
  - `after/projects_confirm_delete_desktop.png` (`role="alertdialog"` confirmation modal with item summary)
  - `after/projects_undo_toast_desktop.png` (`role="status"` toast notification with `Undo Delete` button)
  - `after/mobile_drawer_open.png` (Responsive off-canvas navigation drawer on mobile viewport)
  - `after/contact_desktop.png` (Contact & Inquiries route with bounded log table)
