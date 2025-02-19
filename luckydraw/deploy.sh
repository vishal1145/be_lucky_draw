#!/bin/bash

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev mysql-client

# Install Python requirements
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=production

# Run database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Start the application (using gunicorn in production)
gunicorn -w 4 -b 0.0.0.0:5000 "run:create_app()" 