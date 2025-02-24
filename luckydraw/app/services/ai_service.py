
import requests
from flask import current_app
import random

class AIService:
    @staticmethod
    def evaluate_requirements(requirements_text):
        """
        Evaluate the quality and validity of requirements using DeepSeek API.
        Returns a score between 0-100.
        """
        try:
            api_url = "https://deepseek.algofolks.com/api/chat"
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "deepseek-r1:latest",
                "messages": [
                    {"role": "system", "content": "You are a project requirements evaluator."},
                    {"role": "user", "content": f"Evaluate the following project requirements and rate them on a scale of 0-100 based on clarity, feasibility, and completeness:\n\n{requirements_text}\n\nReturn only the numerical score."}
                ],
                "stream": False
            }
            print("respone by deepseek")

            response = requests.post(api_url, json=payload, headers=headers)
            response_data = response.json()

            if "choices" in response_data and response_data["choices"]:
                score_str = response_data["choices"][0]["message"]["content"].strip()
                score = float(score_str.split()[0]) 
                return min(max(score, 0), 100)

            return random.randint(40, 60)  

        except Exception as e:
            current_app.logger.error(f"AI evaluation error: {str(e)}")
            return random.randint(40, 60)
