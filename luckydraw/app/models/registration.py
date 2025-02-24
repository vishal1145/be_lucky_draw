from app import db
from datetime import datetime
import random
from sqlalchemy.orm import validates
from app.services.ai_service import AIService

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

    COUNTRY_MAPPING = {
        '+44': 'UK',
        '+1': 'US',
        '+91': 'India'
    }

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
        uk_candidates = cls.query.filter_by(country_code='+44').all()
        us_candidates = cls.query.filter_by(country_code='+1').all()
        india_candidates = cls.query.filter_by(country_code='+91').all()

        if not uk_candidates or not us_candidates or not india_candidates:
            return None

        candidates_by_country = {
            'UK': [(candidate, AIService.evaluate_requirements(candidate.requirements)) 
                  for candidate in uk_candidates],
            'US': [(candidate, AIService.evaluate_requirements(candidate.requirements))
                  for candidate in us_candidates],
            'India': [(candidate, AIService.evaluate_requirements(candidate.requirements))
                     for candidate in india_candidates]
        }

        winners_with_scores = []
        for country, candidates in candidates_by_country.items():
            if candidates:
                sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
                winners_with_scores.append((sorted_candidates[0][0], sorted_candidates[0][1], country))  

        winners_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        return winners_with_scores if len(winners_with_scores) == 3 else None