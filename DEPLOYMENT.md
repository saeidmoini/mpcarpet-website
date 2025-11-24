# Deployment Guide

This guide covers the complete deployment process for the Persian Carpet website.

## Prerequisites

- Ubuntu/Debian server
- Python 3.11+
- Nginx
- Gunicorn
- PostgreSQL/SQLite (as configured)

## Initial Setup

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv nginx git
```

### 2. Clone Repository

```bash
cd /home/carpet
git clone <repository-url> mpcarpet-website
cd mpcarpet-website
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Configuration

**CRITICAL:** The `.env` file is NOT in git (it's in `.gitignore`). You must create it manually.

```bash
# Create .env file
nano .env
```

Add the following variables:

```
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,194.33.105.129
CSRF_TRUSTED_ORIGINS=https://your-domain.com,http://194.33.105.129
```

**Set proper permissions:**

```bash
# CRITICAL: Application user (carpet) must be able to read .env
sudo chown carpet:www-data .env
sudo chmod 640 .env
```

### 5. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput

# Set proper ownership and permissions
sudo chown -R carpet:www-data /home/carpet/mpcarpet-website/static/
sudo chmod -R 755 /home/carpet/mpcarpet-website/static/
```

### 7. Gunicorn Service

Create systemd service file:

```bash
sudo nano /etc/systemd/system/persian-carpet.service
```

Add the following:

```ini
[Unit]
Description=Gunicorn daemon for PersianCarpet
After=network.target

[Service]
User=carpet
Group=www-data
WorkingDirectory=/home/carpet/mpcarpet-website
EnvironmentFile=/home/carpet/mpcarpet-website/.env
ExecStart=/home/carpet/mpcarpet-website/venv/bin/gunicorn --workers 3 --bind unix:/run/persian-carpet.sock PersianCarpet.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable persian-carpet.service
sudo systemctl start persian-carpet.service
```

### 8. Nginx Configuration

Create Nginx config:

```bash
sudo nano /etc/nginx/sites-available/persian-carpet
```

Add the following:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com 194.33.105.129;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/carpet/mpcarpet-website/static/;
    }
    
    location /media/ {
        alias /home/carpet/mpcarpet-website/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/persian-carpet.sock;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/persian-carpet /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Updating Deployment

### Standard Update Process

After pulling new changes from git:

```bash
cd /home/carpet/mpcarpet-website

# 1. Pull latest changes
git pull origin main  # or developer branch

# 2. Activate virtual environment
source venv/bin/activate

# 3. Update dependencies (if requirements.txt changed)
pip install -r requirements.txt

# 4. Run migrations (if any)
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Fix permissions for static files
sudo chown -R carpet:www-data /home/carpet/mpcarpet-website/static/
sudo chmod -R 755 /home/carpet/mpcarpet-website/static/

# 7. Fix permissions for .env (IMPORTANT: if .env was recreated or modified)
sudo chown carpet:www-data /home/carpet/mpcarpet-website/.env
sudo chmod 640 /home/carpet/mpcarpet-website/.env

# 8. Restart Gunicorn
sudo systemctl restart persian-carpet.service

# 9. Reload Nginx
sudo systemctl reload nginx
```

### Quick Update Script

You can create a script to automate the update process:

```bash
#!/bin/bash
# save as: /home/carpet/mpcarpet-website/update.sh

cd /home/carpet/mpcarpet-website
source venv/bin/activate

git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

sudo chown -R carpet:www-data /home/carpet/mpcarpet-website/static/
sudo chmod -R 755 /home/carpet/mpcarpet-website/static/
sudo chown carpet:www-data /home/carpet/mpcarpet-website/.env
sudo chmod 640 /home/carpet/mpcarpet-website/.env

sudo systemctl restart persian-carpet.service
sudo systemctl reload nginx

echo "Update complete!"
```

Make it executable:

```bash
chmod +x update.sh
```

## Troubleshooting

### Permission Denied on `.env`

**Error:**

```
PermissionError: [Errno 13] Permission denied: '/home/carpet/mpcarpet-website/.env'
```

**Solution:**

```bash
sudo chown carpet:www-data /home/carpet/mpcarpet-website/.env
sudo chmod 640 /home/carpet/mpcarpet-website/.env
sudo systemctl restart persian-carpet.service
```

### Static Files Not Loading

**Symptoms:**

- 404 errors for CSS/JS/images
- Broken styling on website

**Solution:**

```bash
# Recollect static files
python manage.py collectstatic --noinput --clear

# Fix permissions
sudo chown -R carpet:www-data /home/carpet/mpcarpet-website/static/
sudo chmod -R 755 /home/carpet/mpcarpet-website/static/

# Reload Nginx
sudo systemctl reload nginx
```

### 500 Server Error

**Check Gunicorn logs:**

```bash
sudo journalctl -u persian-carpet.service -n 100 --no-pager
```

**Common causes:**

1. `.env` file permissions (see above)
2. Missing environment variables in `.env`
3. Database migration issues
4. Missing dependencies

**Debug steps:**

```bash
# Check service status
sudo systemctl status persian-carpet.service

# Check Django configuration
python manage.py check

# Test Django directly
python manage.py runserver 0.0.0.0:8000
```

### Gunicorn Not Starting

**Check logs:**

```bash
sudo journalctl -u persian-carpet.service -f
```

**Verify:**

- `.env` file exists and has correct permissions
- Virtual environment is activated
- All dependencies are installed
- Socket file permissions: `sudo chmod 666 /run/persian-carpet.sock`

## Security Notes

1. **Never commit `.env` file** - It's in `.gitignore` for a reason
2. **Set `DEBUG=False`** in production
3. **Use strong `SECRET_KEY`** - Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
4. **Restrict file permissions** - `.env` should be `640`, static files `755`
5. **Keep dependencies updated** - Regularly run `pip install --upgrade -r requirements.txt`

## File Permissions Summary

| File/Directory | Owner | Permissions | Notes |
|---------------|-------|-------------|-------|
| `.env` | carpet:www-data | 640 | Must be readable by application user |
| `static/` | carpet:www-data | 755 | All static files |
| `media/` | carpet:www-data | 755 | User uploaded files |
| `venv/` | carpet:carpet | 755 | Virtual environment |
| Project root | carpet:carpet | 755 | Application files |
