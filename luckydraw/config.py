import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

load_dotenv()

class Config:
    # MySQL Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def _parse_database_url(url):
        """Parse and fix DATABASE_URL to be compatible with PyMySQL"""
        if not url:
            return url
        
        # Parse the URL
        parsed = urlparse(url)
        
        # Convert mysql:// to mysql+pymysql:// for SQLAlchemy
        if parsed.scheme == 'mysql':
            scheme = 'mysql+pymysql'
        else:
            scheme = parsed.scheme
        
        # Parse query parameters
        query_params = parse_qs(parsed.query)
        
        # Remove ssl-mode parameter (PyMySQL doesn't support it)
        if 'ssl-mode' in query_params:
            del query_params['ssl-mode']
        
        # Reconstruct query string
        new_query = urlencode(query_params, doseq=True)
        
        # Reconstruct the URL
        new_parsed = parsed._replace(scheme=scheme, query=new_query)
        return urlunparse(new_parsed)
    
    SQLALCHEMY_DATABASE_URI = _parse_database_url(os.getenv('DATABASE_URL'))

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_ENV') != 'production'

    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

    # Domain Configuration
    DOMAIN_NAME = os.getenv('DOMAIN_NAME')
    
    # Upload folder configuration
    # Use relative path for Fly.io compatibility (workspace directory)
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # CORS Configuration
    # Handle empty string and filter out empty values
    cors_origins_str = os.getenv('CORS_ORIGINS', '')
    CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()] if cors_origins_str else []

    # Static file configuration
    STATIC_FOLDER = 'static'
    STATIC_URL_PATH = '/static'

    def __init__(self):
        # Validate required environment variables
        required_vars = [
            'DATABASE_URL',
            'SECRET_KEY',
            'MAIL_USERNAME',
            'MAIL_PASSWORD',
            'DOMAIN_NAME'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")