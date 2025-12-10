from app.routes import main_bp
from flask import jsonify, request, send_from_directory, render_template, redirect, url_for
from app.controllers.registration_controller import RegistrationController
from app.models.announcement import Announcement
from app.models.registration import Registration
import os
from flask import current_app
from app import db
from datetime import datetime
from app.services.announcement_service import AnnouncementService
from app.services.emailjs_service import EmailJSService

# @main_bp.route('/')
# def index():
#     return jsonify({"message": "Welcome to Lucky Draw API"})

@main_bp.route('/api/register/initiate', methods=['POST'])
def initiate_register():
    if not request.form:
        return jsonify({'error': 'No form data provided'}), 400
        
    return RegistrationController.initiate_verification(request)

# OTP verification disabled - users are registered directly
# @main_bp.route('/api/register/verify', methods=['POST'])
# def verify_registration():
#     data = request.get_json()
#     required_fields = ['temp_id', 'email_otp']
#     for field in required_fields:
#         if field not in data:
#             return jsonify({'error': f'Missing required field: {field}'}), 400
#     return RegistrationController.verify_and_register(data)

@main_bp.route('/api/users', methods=['GET'])
def get_users():
    return RegistrationController.get_all_users()

@main_bp.route('/api/select-winners', methods=['GET'])
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

@main_bp.route('/api/announcement', methods=['GET'])
def get_announcements():
    """Get all announcements or filter by status"""
    try:
        # Get query parameter for status filtering
        # status = request.args.get('status', None)
        
        # if status:
        #     announcements = Announcement.query.filter_by(status=status).order_by(Announcement.announcement_date.desc()).all()
        
        announcements = Announcement.query.order_by(Announcement.announcement_date.desc()).all()
        
        return jsonify({
            'status': 'success',
            'data': [announcement.to_dict() for announcement in announcements]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/announcement', methods=['POST'])
def create_announcement():
    """Create new announcement and delete previous ones"""
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({
                'status': 'error',
                'message': 'title is required'
            }), 400

        # Delete all previous announcements
        try:
            Announcement.query.delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting previous announcements: {str(e)}")

        # Create new announcement
        new_announcement = Announcement(
            title=data.get('title'),
            description=data.get('description'),
            announcement_date=data.get('announcement_date')
        )
        
        db.session.add(new_announcement)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Previous announcements deleted and new announcement created',
            'data': new_announcement.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

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

@main_bp.route('/api/send-announcement-reminders', methods=['GET'])
def send_announcement_reminders():
    """API endpoint to trigger sending announcement reminders"""
    try:
        AnnouncementService.send_announcement_reminders()
        return {
            "status": "success",
            "message": "Announcement reminders sent successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

@main_bp.route('/api/send-results-notification/<int:announcement_id>', methods=['GET'])
def send_results_notification(announcement_id):
    """API endpoint to trigger sending results notification to all users"""
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        AnnouncementService.send_results_notification(announcement)
        return jsonify({
            "status": "success",
            "message": f"Results notification for '{announcement.title}' sent successfully to all users"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


USERNAME = "admin@gmail.com"
PASSWORD = "Algo@987!"
from flask import make_response, redirect, url_for

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']   
        password = request.form['password']

        if email == USERNAME and password == PASSWORD:
            resp = make_response(redirect(url_for('main.registrations')))  
            resp.set_cookie('user_logged_in', 'true')
            return resp  

        else:
            error_message = "Invalid email or password. Please try again."

    return render_template('login.html', error_message=error_message) 


@main_bp.route('/registrations')
def registrations():
    if request.cookies.get('user_logged_in') == 'true':
        
        return RegistrationController.get_registrations_page()

    return redirect(url_for('main.login'))

@main_bp.route('/email-templates')
def email_templates():
    if request.cookies.get('user_logged_in') != 'true':
        return redirect(url_for('main.login'))
    return render_template('email_templates.html')

@main_bp.route('/logout')
def logout():
    resp = make_response(redirect(url_for('main.login')))  
    resp.set_cookie('user_logged_in', '', expires=0)  # Clear the cookie
    return resp

@main_bp.route('/send-bulk-email/<template_type>', methods=['POST'])
def send_bulk_email(template_type):
    if request.cookies.get('user_logged_in') != 'true':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        users = Registration.query.filter_by(is_verified=True).all()
        latest_announcement = Announcement.query.order_by(Announcement.announcement_date.desc()).first()
        
        if not latest_announcement:
            return jsonify({'error': 'No announcements found'}), 404

        successful_sends = 0
        already_sent = 0
        failed_sends = 0

        for user in users:
            # Determine the appropriate email tracking field
            if template_type == 'results':
                last_emailed_field = 'last_results_emailed'
            elif template_type == 'announcement':
                last_emailed_field = 'last_appointment_emailed'
            else:
                return jsonify({'error': 'Invalid template type'}), 400

            # Check if the user has already received this type of email
            last_emailed_value = getattr(user, last_emailed_field)
            if last_emailed_value and last_emailed_value <= latest_announcement.announcement_date:
                already_sent += 1
                continue

            try:
                success = False
                
                if template_type == 'results':
                    success = EmailJSService.send_results_notification(
                        email=user.email,
                        name=user.name,
                        announcement_title=latest_announcement.title,
                        share_url="https://algofolks.com"
                    )
                    
                elif template_type == 'announcement':
                    success = EmailJSService.send_announcement_reminder(
                        email=user.email,
                        name=user.name,
                        announcement_title=latest_announcement.title,
                        announcement_date=latest_announcement.announcement_date,
                        share_url="https://algofolks.com"
                    )
                else:
                    print(f"❌ Invalid email template type for {user.email}, skipping.")
                    failed_sends += 1
                    continue

                if success:
                    # Update the correct email timestamp field
                    setattr(user, last_emailed_field, datetime.utcnow())
                    db.session.commit()
                    successful_sends += 1
                else:
                    failed_sends += 1
                    print(f"Failed to send email to {user.email}")

            except Exception as e:
                failed_sends += 1
                print(f"Failed to send email to {user.email}: {str(e)}")
                continue

            except Exception as e:
                failed_sends += 1
                print(f"Failed to send email to {user.email}: {str(e)}")
                continue
            
        return jsonify({
            'message': 'Email sending completed',
            'stats': {
                'successful': successful_sends,
                'already_sent': already_sent,
                'failed': failed_sends,
                'total_processed': len(users)
            }
        })
        
    except Exception as e:
        print(f"Error in bulk email process: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/debug/emailjs-config', methods=['GET'])
def debug_emailjs_config():
    """Debug endpoint to check EmailJS configuration"""
    if request.cookies.get('user_logged_in') != 'true':
        return jsonify({'error': 'Unauthorized'}), 401
    
    config_status = {
        'EMAILJS_SERVICE_ID': 'SET' if current_app.config.get('EMAILJS_SERVICE_ID') else 'MISSING',
        'EMAILJS_USER_ID': 'SET' if current_app.config.get('EMAILJS_USER_ID') else 'MISSING',
        'EMAILJS_ACCESS_TOKEN': 'SET' if current_app.config.get('EMAILJS_ACCESS_TOKEN') else 'MISSING',
        'EMAILJS_TEMPLATE_GENERIC': current_app.config.get('EMAILJS_TEMPLATE_GENERIC') or 'MISSING',
        'EMAILJS_TEMPLATE_WELCOME': current_app.config.get('EMAILJS_TEMPLATE_WELCOME') or 'MISSING',
    }
    
    return jsonify({
        'status': 'ok',
        'config': config_status,
        'message': 'Check the config values above. All should be SET except template IDs (only one needed)'
    })

@main_bp.route('/api/users/delete-all', methods=['DELETE'])
def delete_all_users():
    """
    Delete all users from the database (for testing purposes)
    Requires admin authentication
    
    Usage:
        DELETE /api/users/delete-all
        Headers: Cookie with user_logged_in=true
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Check authentication
    if request.cookies.get('user_logged_in') != 'true':
        logger.warning("[DELETE_USERS] Unauthorized access attempt")
        return jsonify({'error': 'Unauthorized. Please login as admin.'}), 401
    
    try:
        logger.info("[DELETE_USERS] Starting delete all users operation...")
        
        # Get count before deletion
        total_users = Registration.query.count()
        logger.info(f"[DELETE_USERS] Total users in database: {total_users}")
        
        if total_users == 0:
            logger.info("[DELETE_USERS] No users to delete")
            return jsonify({
                'message': 'No users to delete',
                'deleted_count': 0
            }), 200
        
        # Delete all users
        deleted_count = Registration.query.delete()
        logger.info(f"[DELETE_USERS] Deleted {deleted_count} user(s) from query")
        
        # Commit the transaction
        db.session.commit()
        logger.info(f"[DELETE_USERS] ✅ Successfully committed deletion of {deleted_count} user(s)")
        
        return jsonify({
            'message': f'Successfully deleted {deleted_count} user(s)',
            'deleted_count': deleted_count,
            'total_users_before': total_users
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"[DELETE_USERS] ❌ Error deleting users: {str(e)}")
        import traceback
        logger.error(f"[DELETE_USERS] Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Failed to delete users',
            'message': str(e)
        }), 500
