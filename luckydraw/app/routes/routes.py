from app.routes import main_bp
from flask import jsonify, request
from app.controllers.registration_controller import RegistrationController

@main_bp.route('/')
def index():
    return jsonify({"message": "Welcome to Lucky Draw API"})

@main_bp.route('/api/register/initiate', methods=['POST'])
def initiate_register():
    data = request.get_json()
    
    required_fields = ['name', 'email', 'phone', 'requirement', 'preferredTechnology']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
            
    return RegistrationController.initiate_registration(data)

@main_bp.route('/api/register/verify', methods=['POST'])
def verify_registration():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
        
    data = request.get_json()
    
    required_fields = ['temp_id', 'email_otp']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
            
    return RegistrationController.verify_otp(data)

@main_bp.route('/api/send-email-otp', methods=['POST'])
def send_email_otp():
    data = request.get_json()
    if 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    return RegistrationController.send_email_otp(data)

@main_bp.route('/api/send-phone-otp', methods=['POST'])
def send_phone_otp():
    data = request.get_json()
    if 'phone' not in data:
        return jsonify({'error': 'Phone number is required'}), 400
    return RegistrationController.send_phone_otp(data)

@main_bp.route('/api/register/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json()
    required_fields = ['temp_id', 'email_otp']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    return RegistrationController.verify_email(data)

@main_bp.route('/api/register/verify-phone', methods=['POST'])
def verify_phone():
    data = request.get_json()
    required_fields = ['temp_id', 'phone_otp']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    return RegistrationController.verify_phone(data)

@main_bp.route('/api/register/complete', methods=['POST'])
def complete_registration():
    data = request.get_json()
    if 'temp_id' not in data:
        return jsonify({'error': 'Missing temp_id'}), 400
    return RegistrationController.complete_registration(data)

@main_bp.route('/api/users', methods=['GET'])
def get_users():
    return RegistrationController.get_all_users()

@main_bp.route('/api/select-winners', methods=['POST'])
def select_winners():
    return RegistrationController.select_winners() 