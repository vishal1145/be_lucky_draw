from app import db
from datetime import datetime
import random

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    technologies = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.mobile_number
        }

    @classmethod
    def select_winners(cls, count=3):
        all_users = cls.query.all()
        if len(all_users) < count:
            return all_users
        return random.sample(all_users, count) 