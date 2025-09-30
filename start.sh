#!/bin/bash

# Email Classifier - Render Start Script
set -e

echo "🚀 Starting Email Classifier application..."

# Run database migrations if needed
echo "🔧 Running database setup..."
python3 migrate_db.py

# Start the application with Gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --preload run:app