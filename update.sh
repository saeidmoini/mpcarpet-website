#!/bin/bash
# Update script for Persian Carpet website deployment
# Usage: ./update.sh [branch]
# Default branch: main

BRANCH=${1:-main}
PROJECT_DIR="/home/carpet/mpcarpet-website"
STATIC_DIR="$PROJECT_DIR/static"
DB_FILE="$PROJECT_DIR/project.db"

echo "========================================="
echo "Persian Carpet Website Update Script"
echo "========================================="
echo "Branch: $BRANCH"
echo "Project Directory: $PROJECT_DIR"
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Error: This script must be run as root or with sudo"
    exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR" || {
    echo "Error: Cannot access project directory: $PROJECT_DIR"
    exit 1
}

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || {
    echo "Error: Cannot activate virtual environment"
    exit 1
}

# Pull latest changes
echo "Pulling latest changes from $BRANCH..."
git pull origin "$BRANCH" || {
    echo "Error: Git pull failed"
    exit 1
}

# Update dependencies
echo "Updating dependencies..."
pip install -r requirements.txt || {
    echo "Warning: Some dependencies may have failed to install"
}

# Run migrations
echo "Running database migrations..."
python manage.py migrate || {
    echo "Error: Migrations failed"
    exit 1
}

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || {
    echo "Error: collectstatic failed"
    exit 1
}

# Fix permissions for project directory and database
echo "Fixing permissions for project directory and database..."
chown carpet:carpet "$PROJECT_DIR" || {
    echo "Warning: Failed to change ownership of project directory"
}
chmod 775 "$PROJECT_DIR" || {
    echo "Warning: Failed to change permissions of project directory"
}
if [ -f "$DB_FILE" ]; then
    chown carpet:carpet "$DB_FILE" || {
        echo "Warning: Failed to change ownership of project.db"
    }
    chmod 664 "$DB_FILE" || {
        echo "Warning: Failed to change permissions of project.db"
    }
    # Remove SQLite lock files if present
    rm -f "${DB_FILE}-shm" "${DB_FILE}-wal"
fi

# Fix permissions for static files
echo "Fixing permissions for static files..."
chown -R carpet:www-data "$STATIC_DIR" || {
    echo "Warning: Failed to change ownership of static files"
}
chmod -R 755 "$STATIC_DIR" || {
    echo "Warning: Failed to change permissions of static files"
}

# Fix permissions for .env file
if [ -f "$PROJECT_DIR/.env" ]; then
    echo "Fixing permissions for .env file..."
    chown carpet:www-data "$PROJECT_DIR/.env" || {
        echo "Warning: Failed to change ownership of .env"
    }
    chmod 640 "$PROJECT_DIR/.env" || {
        echo "Warning: Failed to change permissions of .env"
    }
else
    echo "Warning: .env file not found!"
fi

# Restart Gunicorn service
echo "Restarting Gunicorn service..."
systemctl restart persian-carpet.service || {
    echo "Error: Failed to restart Gunicorn service"
    exit 1
}

# Check Gunicorn status
sleep 2
if systemctl is-active --quiet persian-carpet.service; then
    echo "✓ Gunicorn service is running"
else
    echo "✗ Error: Gunicorn service is not running"
    echo "Check logs with: sudo journalctl -u persian-carpet.service -n 50"
    exit 1
fi

# Reload Nginx
echo "Reloading Nginx..."
systemctl reload nginx || {
    echo "Warning: Failed to reload Nginx"
}

echo ""
echo "========================================="
echo "Update completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Check website: http://your-domain.com"
echo "2. Check Gunicorn logs: sudo journalctl -u persian-carpet.service -n 50"
echo "3. Check Nginx logs: sudo tail -f /var/log/nginx/error.log"
echo ""
