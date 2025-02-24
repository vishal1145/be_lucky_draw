from openai import OpenAI
from flask import current_app
import random

class AIService:
    @staticmethod
    def evaluate_requirements(requirements_text):
        """
        Evaluate the quality and validity of requirements using GPT
        Returns a score between 0-100
        """
        try:
            client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
            
            prompt = f"""
            Evaluate the following project requirements and rate them on a scale of 0-100 
            based on clarity, feasibility, and completeness:

            {requirements_text}

            Return only the numerical score.
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a project requirements evaluator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.3
            )

            score_str = response.choices[0].message.content.strip()
            score = float(score_str.split()[0]) 
            return min(max(score, 0), 100) 

        except Exception as e:
            current_app.logger.error(f"AI evaluation error: {str(e)}")
            return random.randint(40, 60) 

        
