from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from app.services.email_service import mail
from dotenv import load_dotenv
import os
import pymysql

# Load environment variables from .env file
load_dotenv()

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
    
    # Enable CORS using configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
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
    
    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app