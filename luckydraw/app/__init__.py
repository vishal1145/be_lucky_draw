from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Import models to ensure they're registered with SQLAlchemy
    from app.models import registration, otp
    
    # Create database tables
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
        except Exception as e:
            print(f"Database Error: {e}")
            print("Please ensure MySQL is running and the database exists")
    
    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app