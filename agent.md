# Persian Carpet – Agent Log

## Phase 1 – 2025-11-10

- Set `LANGUAGE_CODE` to Farsi and restricted active languages to prevent `/en/` URL prefixes.
- Disabled default language prefixes in `i18n_patterns` for clean Farsi routes.
- Pointed the root URL and `/home/` alias to the slider-based home template; exposed the video prototype at `/home-video/`.
- Updated project documentation (`README.md`) with the current phase summary and developer notes.

### Notes for Next Phase

- Introduce a shared base template and restructure page templates to extend it.
- Normalize navbar/footer includes (remove embedded `<head>` tags) and fix link targets using Django `url` tags.
- Consolidate font assets and audit static references ahead of responsive adjustments.

## Phase 2 – 2025-11-10

- Introduced a reusable `base.html` plus shared navbar/footer includes and migrated the home (slider + video), products, about, and contact templates to extend it while preserving their Figma markup.
- Updated docs to reflect ongoing template migration and the plan for visual regression safeguards.

### Notes for Next Phase

- Consolidate fonts/assets under consistent static paths and replace bare `img/...` references with `{% static %}`.
- Introduce responsive breakpoints and accessibility tweaks while maintaining Figma alignment.
- Prepare data structures or CMS placeholders for dynamic content (gallery, products, contact form).

## Phase 3 – 2025-11-10

- Collapsed duplicate IRANYekan font directories into `PersianCarpet/static/fonts/IRYekan` and expanded `fonts.css` to serve WOFF/WOFF2 sources with `font-display: swap`.
- Migrated remaining inline `<style>` blocks into the appropriate static stylesheets and wired navigation/contact links through `{% url %}` helpers.
- Added responsive breakpoints (scale-down strategy + targeted tweaks) for the home, products, about, and contact templates.
- Extracted shared contact details into `components/fragments/` includes to ease the eventual CMS hand-off, and refreshed the README Phase 3 summary.

### Notes for Next Phase

- Parameterise the new fragments via context or CMS models once templates move off static copy.
- Replace scale-based responsive fallback with semantic layout tweaks once design sign-off allows structural adjustments.
- Connect gallery/product CTAs to dynamic slugs when the CMS schema is defined.
