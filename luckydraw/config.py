import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database URI from environment variables with fallback
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
    #     'mysql+pymysql://root:Algofolks123@localhost:3306/lottery?unix_socket=/opt/lampp/var/mysql/mysql.sock')

    # SQLALCHEMY_DATABASE_URI = f"mysql://root:Algo1234!@localhost/lucky_draw"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Algofolks123@localhost:3306/lottery?unix_socket=/opt/lampp/var/mysql/mysql.sock'

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.environ.get('FLASK_ENV') != 'production'

    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'coder.rajat07@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'somq fgrb ndou gfdy')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'coder.rajat07@gmail.com')

    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'your_twilio_number')

    # Domain Configuration
    DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'https://lucky-draw.algofolks.com')
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8080,http://localhost:5173,https://lucky-draw.algofolks.com').split(',')