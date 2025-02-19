from app.routes import main_bp
from flask import jsonify, request
from app.controllers.registration_controller import RegistrationController

@main_bp.route('/')
def index():
    return jsonify({"message": "Welcome to Lucky Draw API"})

@main_bp.route('/api/register/initiate', methods=['POST'])
def initiate_register():
    data = request.get_json()
    
    required_fields = ['name', 'email', 'country_code', 'phone', 'technologies', 'requirements']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
            
    return RegistrationController.initiate_verification(data)

@main_bp.route('/api/register/verify', methods=['POST'])
def verify_registration():
    data = request.get_json()
    required_fields = ['temp_id', 'email_otp', 'phone_otp']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    return RegistrationController.verify_and_register(data)

@main_bp.route('/api/users', methods=['GET'])
def get_users():
    return RegistrationController.get_all_users()

@main_bp.route('/api/select-winners', methods=['POST'])
def select_winners():
    return RegistrationController.select_winners() 