#!/bin/bash
set -euo pipefail

# Usage: ./update.sh [branch]
# Default branch: developer

BRANCH=${1:-developer}
PROJECT_DIR="/home/carpet/mpcarpet-website"
STATIC_DIR="$PROJECT_DIR/static"
DB_FILE="$PROJECT_DIR/project.db"
VENV="$PROJECT_DIR/venv"
SERVICE="persian-carpet.service"
APP_USER="carpet"
APP_GROUP="www-data"

echo "========================================="
echo "Persian Carpet Website Update Script"
echo "========================================="
echo "Branch: $BRANCH"
echo "Project Directory: $PROJECT_DIR"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo "Error: This script must be run as root (use sudo)."
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory not found: $PROJECT_DIR"
    exit 1
fi

run_as_app() {
    sudo -u "$APP_USER" -H bash -lc "$*"
}

cd "$PROJECT_DIR"

# Protect local SQLite DB from git complaints (no data deletion)
if [ -f "$DB_FILE" ]; then
    run_as_app "cd '$PROJECT_DIR' && git update-index --skip-worktree project.db || true"
fi

echo "Updating repository to origin/$BRANCH..."
run_as_app "cd '$PROJECT_DIR' && git fetch origin '$BRANCH'"
run_as_app "cd '$PROJECT_DIR' && git reset --hard 'origin/$BRANCH'"

echo "Activating virtual environment and installing dependencies..."
run_as_app "source '$VENV/bin/activate' && cd '$PROJECT_DIR' && pip install -r requirements.txt"

echo "Running migrations..."
run_as_app "source '$VENV/bin/activate' && cd '$PROJECT_DIR' && python manage.py migrate --noinput"

echo "Collecting static files..."
run_as_app "source '$VENV/bin/activate' && cd '$PROJECT_DIR' && python manage.py collectstatic --noinput"

echo "Fixing permissions..."
chown -R "$APP_USER:$APP_GROUP" "$PROJECT_DIR"
chmod 775 "$PROJECT_DIR"
if [ -f "$DB_FILE" ]; then
    chmod 664 "$DB_FILE"
    rm -f "${DB_FILE}-shm" "${DB_FILE}-wal"
fi
if [ -f "$PROJECT_DIR/.env" ]; then
    chown "$APP_USER:$APP_GROUP" "$PROJECT_DIR/.env"
    chmod 640 "$PROJECT_DIR/.env"
fi
if [ -d "$STATIC_DIR" ]; then
    chown -R "$APP_USER:$APP_GROUP" "$STATIC_DIR"
    chmod -R 755 "$STATIC_DIR"
fi

echo "Restarting services..."
systemctl restart "$SERVICE"
systemctl reload nginx || true

echo "Done."
