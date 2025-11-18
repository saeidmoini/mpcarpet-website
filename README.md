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

Static assets are collected from `PersianCarpet/static` and served under `/static/`. For local development, ensure `DEBUG=True` in `.env` to enable Django's static file handling.

## Deployment

### Initial Server Setup

1. **Clone and setup:**

```bash
git clone <repository-url>
cd mpcarpet-website
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Create `.env` file:**

```bash
# Create .env file with required variables
# IMPORTANT: .env is in .gitignore and should NOT be committed
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com
EOF
```

3. **Set proper permissions for `.env`:**

```bash
# CRITICAL: .env must be readable by the application user (carpet)
sudo chown carpet:www-data .env
sudo chmod 640 .env
```

4. **Run migrations:**

```bash
python manage.py migrate
```

5. **Collect static files:**

```bash
python manage.py collectstatic --noinput
# Set proper ownership for static files
sudo chown -R carpet:www-data /path/to/static/
sudo chmod -R 755 /path/to/static/
```

### After Pulling Updates

**IMPORTANT:** After pulling new changes from git, always run:

```bash
# 1. Pull latest changes
git pull origin main  # or developer branch

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install/update dependencies (if requirements.txt changed)
pip install -r requirements.txt

# 4. Run migrations (if any)
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Fix permissions for static files
sudo chown -R carpet:www-data /path/to/static/
sudo chmod -R 755 /path/to/static/

# 7. Fix permissions for .env (if it was recreated)
sudo chown carpet:www-data .env
sudo chmod 640 .env

# 8. Restart Gunicorn service
sudo systemctl restart persian-carpet.service

# 9. Reload Nginx
sudo systemctl reload nginx
```

### Common Issues

**Permission Denied on `.env`:**

- Error: `PermissionError: [Errno 13] Permission denied: '/path/to/.env'`
- Solution: `sudo chown carpet:www-data .env && sudo chmod 640 .env`

**Static files not loading:**

- Check permissions: `sudo chown -R carpet:www-data /path/to/static/`
- Verify collectstatic ran: `python manage.py collectstatic --noinput`
- Check Nginx config points to correct static path

**500 Server Error:**

- Check Gunicorn logs: `sudo journalctl -u persian-carpet.service -n 100`
- Verify `.env` permissions and content
- Ensure all migrations are applied: `python manage.py migrate`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).
