class Config:
    # MySQL Database Configuration
    SQLALCHEMY_DATABASE_URI = f"mysql://root:Algo1234!@localhost/lucky_draw"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask Configuration
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True

    # Email Configuration (using Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'coder.rajat07@gmail.com' 
    MAIL_PASSWORD = 'somq fgrb ndou gfdy'     
    MAIL_DEFAULT_SENDER = 'coder.rajat07@gmail.com' 