#!/bin/bash

echo "🚀 Starting Email Classifier with custom gunicorn config..."
echo "🔧 Port: ${PORT:-10000}"
echo "🔧 Command: gunicorn --config gunicorn_config.py run:app"

exec gunicorn --config gunicorn_config.py run:app