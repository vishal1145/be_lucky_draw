from app import db
from datetime import datetime, timedelta
import random

class OTP(db.Model):
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email_otp = db.Column(db.String(6), nullable=False)
    phone_otp = db.Column(db.String(6), nullable=False)
    technologies = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    image_url = db.Column(db.String(255))

    def __init__(self, data):
        self.name = data.get('name')
        self.email = data.get('email')
        self.country_code = data.get('country_code')
        self.phone = data.get('phone')
        self.technologies = data.get('technologies')
        self.requirements = data.get('requirements')
        self.image_url = data.get('image_url')
        self.email_otp = str(random.randint(100000, 999999))
        self.phone_otp = 123456
        # self.phone_otp = str(random.randint(100000, 999999))
        self.expires_at = datetime.utcnow() + timedelta(minutes=10)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999)) 