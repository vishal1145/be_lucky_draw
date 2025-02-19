#!/bin/bash

# Install requirements
pip install -r requirements.txt

# Set environment variable
export FLASK_APP=run.py

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Start the application
flask run 