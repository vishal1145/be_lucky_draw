from app import db
from datetime import datetime, timedelta

class OTP(db.Model):
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email_otp = db.Column(db.String(6), nullable=False)
    phone_otp = db.Column(db.String(6), nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    registration_data = db.Column(db.JSON, nullable=False)

    def __init__(self, email, phone, registration_data):
        self.email = email
        self.phone = phone
        self.email_otp = self.generate_otp()
        self.phone_otp = self.generate_otp()
        self.expires_at = datetime.utcnow() + timedelta(minutes=10)
        self.registration_data = registration_data

    @staticmethod
    def generate_otp():
        import random
        return str(random.randint(100000, 999999)) 