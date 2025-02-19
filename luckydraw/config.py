import os

class Config:
    # MySQL Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'mysql+pymysql://root:Trading123@localhost:3306/lucky_draw_db?unix_socket=/opt/lampp/var/mysql/mysql.sock'
    )
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = True

    # Email Configuration (using Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'coder.rajat07@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'somq fgrb ndou gfdy'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'coder.rajat07@gmail.com'

    # Twilio Configuration (for future use)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID') or 'your_account_sid'
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN') or 'your_auth_token'
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER') or 'your_twilio_number'