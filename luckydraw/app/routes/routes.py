from app.routes import main_bp
from flask import jsonify, request, send_from_directory
from app.controllers.registration_controller import RegistrationController
import os
from flask import current_app

@main_bp.route('/')
def index():
    return jsonify({"message": "Welcome to Lucky Draw API"})

@main_bp.route('/api/register/initiate', methods=['POST'])
def initiate_register():
    if not request.form:
        return jsonify({'error': 'No form data provided'}), 400
        
    return RegistrationController.initiate_verification(request)

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

@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename) 