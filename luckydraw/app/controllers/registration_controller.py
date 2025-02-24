from app import db
from app.models.registration import Registration
from app.models.otp import OTP
from flask import jsonify, current_app, request
from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from app.utils.file_helpers import allowed_file
from app.models.announcement import Announcement
class RegistrationController:
    @staticmethod
    def initiate_verification(data):
        try:
            
            # Get form data
            form_data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'country_code': request.form.get('country_code'),
                'phone': request.form.get('phone'),
                'technologies': request.form.get('technologies'),
                'requirements': request.form.get('requirements')
            }

            # Validate required fields
            required_fields = ['name', 'email', 'country_code', 'phone', 'technologies', 'requirements']
            for field in required_fields:
                if not form_data.get(field):
                    return jsonify({'error': f'Missing required field: {field}'}), 400

            # Check for existing email
            existing_registration = Registration.query.filter_by(email=form_data['email']).first()
            if existing_registration:
                return jsonify({
                    'error': 'Email already registered'
                }), 200

            # Check for existing phone number
            existing_phone = Registration.query.filter_by(mobile_number=form_data['phone']).first()
            if existing_phone:
                return jsonify({
                    'error': 'Phone number already registered'
                }), 200

            # Handle image upload
            image = request.files.get('image')
            image_url = None
            
            if image:
                if not allowed_file(image.filename):
                    return jsonify({
                        'error': 'Invalid file type. Allowed types are: png, jpg, jpeg, gif'
                    }), 400
                
                try:
                    filename = secure_filename(image.filename)
                    unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    image_path = os.path.join(upload_folder, unique_filename)
                    image.save(image_path)
                    
                    # Generate full URL with domain
                    domain = current_app.config.get('DOMAIN_NAME', '').rstrip('/')
                    if not domain:
                        return jsonify({
                            'error': 'Server configuration error: DOMAIN_NAME not set'
                        }), 500
                    
                    image_url = f"{domain}/uploads/{unique_filename}"

                except Exception as e:
                    return jsonify({
                        'error': 'Failed to save image',
                        'message': str(e)
                    }), 500

            # Add image_url to form_data
            form_data['image_url'] = image_url

            # Create OTP record with all user data
            otp_record = OTP(form_data)
            db.session.add(otp_record)
            db.session.commit()
            
            # Send email OTP
            email_sent = EmailService.send_otp_email(
                email=form_data.get('email'),
                otp=otp_record.email_otp
            )
            
            # Send SMS OTP
            sms_sent = SMSService.send_otp_sms(
                phone_number=f"{form_data.get('country_code')}{form_data.get('phone')}",
                otp=otp_record.phone_otp
            )
            
            if not email_sent or not sms_sent:
                db.session.delete(otp_record)
                db.session.commit()
                return jsonify({
                    'error': 'Failed to send OTPs'
                }), 500

            return jsonify({
                'message': 'OTPs sent successfully',
                'temp_id': otp_record.id
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Failed to initiate verification',
                'message': str(e)
            }), 400

    @staticmethod
    def verify_and_register(data):
        try:
            temp_id = data.get('temp_id')
            email_otp = data.get('email_otp')
            phone_otp = data.get('phone_otp')

            otp_record = OTP.query.get(temp_id)

            if not otp_record:
                return jsonify({'error': 'Invalid temporary ID'}), 400

            if datetime.utcnow() > otp_record.expires_at:
                return jsonify({'error': 'OTPs expired'}), 400

            if email_otp != otp_record.email_otp:
                return jsonify({'error': 'Invalid email OTP'}), 400

            if phone_otp != otp_record.phone_otp:
                return jsonify({'error': 'Invalid phone OTP'}), 400

            # Fetch the latest announcement date
            latest_announcement = Announcement.query.order_by(Announcement.announcement_date.desc()).first()
            if not latest_announcement:
                return jsonify({'error': 'No announcements found'}), 400

            # Check if registration_date is within 1 day from announcement_date
            announcement_date = latest_announcement.announcement_date
            registration_date = datetime.utcnow()

            # Allow registration ONLY one day before the announcement date
            allowed_registration_date = announcement_date - timedelta(days=1)

            if registration_date == allowed_registration_date:
                return jsonify({'error': 'Registration is only allowed one day before the announcement date'}), 403

            # Create registration
            new_registration = Registration(
                name=otp_record.name,
                email=otp_record.email,
                country_code=otp_record.country_code,
                mobile_number=otp_record.phone,
                technologies=otp_record.technologies,
                requirements=otp_record.requirements,
                image_url=otp_record.image_url,
                registration_date=registration_date
            )

            db.session.add(new_registration)
            db.session.delete(otp_record)
            db.session.commit()

            # Send welcome email
            EmailService.send_welcome_email(
                email=new_registration.email,
                name=new_registration.name
            )

            return jsonify({
                'message': 'Registration successful!',
                'user_id': new_registration.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Verification failed',
                'message': str(e)
            }), 400


    @staticmethod
    def get_all_users():
        try:
            users = Registration.query.all()
            user_count = Registration.query.count()
            users_list = [user.to_dict() for user in users]
            return jsonify({"users": users_list, "no_of_users": user_count}), 200
        except Exception as e:
            return jsonify({
                'error': 'Failed to fetch users',
                'message': str(e)
            }), 500

    @staticmethod
    def select_winners():
        try:
            winners_data = Registration.select_winners(3)
            
            if not winners_data:
                return jsonify({
                    'error': 'Unable to select winners. Ensure there are eligible candidates from UK (+44), US (+1), and India (+91)'
                }), 404

            response_data = []
            for index, (winner, score, country) in enumerate(winners_data, 1):
                EmailService.send_winner_email(
                    email=winner.email,
                    name=winner.name
                )
                
                SMSService.send_winner_sms(
                    phone_number=f"{winner.country_code}{winner.mobile_number}",
                    name=winner.name
                )
                
                response_data.append({
                    "position": index,  
                    "name": winner.name,
                    "email": winner.email,
                    "phone": winner.mobile_number,
                    "country": country,
                    "requirements": winner.requirements,
                    "requirement_score": round(score, 2) 
                })

            return jsonify({
                'message': 'Winners selected and notified!',
                'winners': response_data
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Failed to select winners',
                'message': str(e)
            }), 500 