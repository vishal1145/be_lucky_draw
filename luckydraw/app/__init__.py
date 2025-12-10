from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from app.services.email_service import mail
from dotenv import load_dotenv
import os
import pymysql
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

pymysql.install_as_MySQLdb()

def create_app(config_class=Config):
    # Initialize app with static folder explicitly defined
    app = Flask(__name__,
                static_folder='static',
                static_url_path='/static')
    
    # Load configuration first
    app.config.from_object(config_class)
    
    # Enable CORS - Simple and permissive configuration
    # Allow all origins for easy development and testing
    cors_origins = app.config.get('CORS_ORIGINS', [])
    
    # All common browser headers
    allowed_headers = [
        "Content-Type", "Authorization", "Accept", "Accept-Language",
        "Origin", "Referer", "Sec-Ch-Ua", "Sec-Ch-Ua-Mobile",
        "Sec-Ch-Ua-Platform", "Sec-Fetch-Dest", "Sec-Fetch-Mode",
        "Sec-Fetch-Site", "User-Agent", "X-Requested-With",
        "Access-Control-Request-Method", "Access-Control-Request-Headers"
    ]
    
    if not cors_origins:
        # Allow all origins (wildcard) - works for both dev and prod
        CORS(app, 
             resources={r"/api/*": {
                 "origins": "*",
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                 "allow_headers": allowed_headers,
                 "expose_headers": ["Content-Type", "Content-Length"],
                 "supports_credentials": False,
                 "max_age": 3600
             }})
    else:
        # Use specific origins from environment
        CORS(app,
             resources={r"/api/*": {
                 "origins": cors_origins,
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                 "allow_headers": allowed_headers,
                 "expose_headers": ["Content-Type", "Content-Length"],
                 "supports_credentials": True,
                 "max_age": 3600
             }})
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Ensure static/images/emails folder exists
    os.makedirs(os.path.join(app.static_folder, 'images', 'emails'), exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Import models to ensure they're registered with SQLAlchemy
    from app.models import registration, otp, announcement
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database Error: {e}")
            print("Please ensure MySQL is running and the database exists")
    
    # Add manual CORS headers - ensure they're always set
    @app.after_request
    def after_request(response):
        # Get origin from request
        origin = request.headers.get('Origin', '*')
        
        # Allow all origins if no CORS_ORIGINS is set, otherwise check against list
        cors_origins = app.config.get('CORS_ORIGINS', [])
        
        # CRITICAL: Always set Access-Control-Allow-Origin
        if not cors_origins:
            # Allow all origins (wildcard)
            response.headers['Access-Control-Allow-Origin'] = '*'
        else:
            # Allow specific origin if it's in the list, otherwise use the request origin
            if origin and origin in cors_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
            elif origin:
                # If origin is provided but not in list, still allow it for development
                response.headers['Access-Control-Allow-Origin'] = origin
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
        
        # Always set these headers
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Accept-Language, Origin, Referer, Sec-Ch-Ua, Sec-Ch-Ua-Mobile, Sec-Ch-Ua-Platform, Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, User-Agent, X-Requested-With'
        response.headers['Access-Control-Max-Age'] = '3600'
        
        # Handle preflight OPTIONS request
        if request.method == 'OPTIONS':
            response.status_code = 200
        
        return response
    
    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app