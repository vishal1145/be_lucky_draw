#!/bin/bash

# Set Flask application
export FLASK_APP=wsgi.py

# Ensure all packages are installed
pip install -r requirements.txt

# Run migrations
echo "Initializing database migrations..."
flask db init

echo "Creating initial migration..."
flask db migrate -m "initial migration"

echo "Applying migrations..."
flask db upgrade

echo "Database setup complete!" 