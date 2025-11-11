# Persian Carpet Website

Persian Carpet is a Django CMS driven marketing site that mirrors a pixel-perfect
Figma design for a Persian carpet manufacturer. The project is being refactored
in incremental phases to improve maintainability while preserving the approved UI.

## Current Phase Summary

### Phase 1 – Localization & Routing (Completed)
- Default language switched to Farsi and CMS language configuration aligned to a single-language site.
- Internationalized URL prefixes disabled until additional locales are ready.
- Slider-based home page is now the default at `/`, with `/home/` as an alias and the video variant available at `/home-video/`.

### Phase 2 – Template Architecture (In Progress)
- Base scaffolding (`base.html`, shared navbar/footer includes) is in place, and the home, video-home, about, contact, and products templates now extend it while keeping their Figma markup intact.
- Remaining pages will be migrated once we have automated regression checks to guarantee no visual drift.

### Phase 3 – Asset Cleanup (In Progress)
- Consolidated IRANYekan font files under `PersianCarpet/static/fonts/IRYekan` and updated `fonts.css` to serve WOFF/WOFF2 sources.
- Audited templates for hard-coded assets: fixed mis-cased references, enforced `{% static %}` usage, and removed residual inline styles in favour of page stylesheets.
- Added responsive breakpoints for home, products, about, and contact layouts while keeping the desktop composition pixel-aligned.
- Introduced fragment includes for shared contact details to prepare for CMS-driven content blocks.

### Upcoming Focus
- Continue Phase 2 refactor with visual regression guardrails.
- Phase 3 follow-ups: replace hard-coded contact copy with context variables, wire navigation CTAs to future CMS slugs, and validate responsive behaviour with screenshot regression.

## Development Notes

- **Localization:** `LANGUAGE_CODE` is `fa`; add future locales in `PersianCarpet/settings.py` under `LANGUAGES` and `CMS_LANGUAGES`.
- **Routing:** Template-driven pages are temporarily exposed via `TemplateView` definitions in `PersianCarpet/urls.py`. CMS URLs remain mounted for future content management.
- **Home Variants:** `/` and `/home/` serve the slider experience. `/home-video/` keeps the video prototype accessible for evaluation.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Static assets are collected from `PersianCarpet/static` and served under `/static/`. For local development, ensure `DEBUG=True` in `.env` to enable Django’s static file handling.
