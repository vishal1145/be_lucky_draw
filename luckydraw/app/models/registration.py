from app import db
from datetime import datetime
import random
from sqlalchemy.orm import validates

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    mobile_number = db.Column(db.String(20),unique=True, nullable=False)
    technologies = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships

    def __repr__(self):
        return f'<Registration {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'country_code': self.country_code,
            'phone': self.mobile_number,
            'technologies': self.technologies,
            'requirements': self.requirements,
            'image_url': self.image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'is_verified': self.is_verified,
            'is_active': self.is_active
        }

    @classmethod
    def select_winners(cls, count=3):
        all_users = cls.query.all()
        if len(all_users) < count:
            return all_users
        return random.sample(all_users, count)