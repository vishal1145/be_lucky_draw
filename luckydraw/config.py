import os

class Config:
    # MySQL Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database URI will be different for local and server
    if os.environ.get('FLASK_ENV') == 'production':
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Trading123@localhost:3306/lucky?unix_socket=/opt/lampp/var/mysql/mysql.sock'
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql://root:Algo1234!@localhost/lucky_draw'
    
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = os.environ.get('FLASK_ENV') != 'production'

    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'coder.rajat07@gmail.com'
    MAIL_PASSWORD = 'somq fgrb ndou gfdy'
    MAIL_DEFAULT_SENDER = 'coder.rajat07@gmail.com'

    # Twilio Configuration (for future use)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID') or 'your_account_sid'
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN') or 'your_auth_token'
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER') or 'your_twilio_number'