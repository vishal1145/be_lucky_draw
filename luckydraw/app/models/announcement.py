from app import db
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import validates

class Announcement(db.Model):
    __tablename__ = 'announcement'
    
    id = db.Column(db.Integer, primary_key=True)
    announcement_date = db.Column(db.DateTime,nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'announcement_date': self.announcement_date.strftime('%Y-%m-%d %H:%M:%S'),
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is required')
        if len(title) > 200:
            raise ValueError('Title must be less than 200 characters')
        return title

    @classmethod
    def get_upcoming_announcements(cls, days_ahead=3):
        target_date = datetime.utcnow() + timedelta(days=days_ahead)
        return cls.query.filter(
            cls.announcement_date >= target_date,
            cls.announcement_date < target_date + timedelta(days=1)
        ).all()
