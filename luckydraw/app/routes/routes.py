from app.routes import main_bp
from flask import jsonify, request, send_from_directory, render_template
from app.controllers.registration_controller import RegistrationController
from app.models.announcement import Announcement
import os
from flask import current_app
from app import db
from datetime import datetime
from app.services.announcement_service import AnnouncementService

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

@main_bp.route('/api/announcement-email')
def get_welcome_email():
    # Get the latest announcement from database
    latest_announcement = Announcement.query.order_by(Announcement.announcement_date.desc()).first()
    
    if not latest_announcement:
        # Fallback to sample data if no announcement exists
        latest_announcement = {
            'title': 'Sample Announcement',
            'description': 'This is a sample announcement for email template preview',
            'announcement_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    return render_template('emails/announcement_reminder.html', 
                         announcement=latest_announcement,
                         name="Test User",
                         share_url="https://algofolks.com")


@main_bp.route('/api/announcement',methods=['POST'])
def create_announcement():
   try:
       data = request.get_json()        
       if not data or 'title' not in data:
           return jsonify({
               'status':'error',
               'message':'title is required'
           }),200
       new_announcement = Announcement(
           title=data.get('title'),
           description=data.get('description'),
           announcement_date=data.get('announcement_date')
       )
       db.session.add(new_announcement)
       db.session.commit()
       return jsonify({
           'status':"success",
           'message':new_announcement.to_dict()

       }),201
   except Exception as e:
       db.session.rollback()
       return jsonify({
           'status':'error',
           'message':str(e)
       }),500

@main_bp.route('/test/email/results/<int:announcement_id>')
def test_results_email(announcement_id):
    """Preview the results notification email template in browser"""
    announcement = Announcement.query.get_or_404(announcement_id)
    return render_template(
        'emails/results_notification.html',
        announcement=announcement,
        name="Test User"
    )

@main_bp.route('/api/test/send-results/<int:announcement_id>')
def test_send_results_notification(announcement_id):
    """Test API endpoint to send results notification email"""
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        AnnouncementService.send_results_notification(announcement)
        return {
            "status": "success",
            "message": "Results notification sent successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500
