from app import db
from app.models.registration import Registration
from app.models.otp import OTP
from flask import jsonify
from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from datetime import datetime, timedelta

class RegistrationController:
    @staticmethod
    def send_email_otp(data):
        try:
            email = data.get('email')
            
            # Check if email already exists
            existing_registration = Registration.query.filter_by(email=email).first()
            if existing_registration:
                return jsonify({
                    'error': 'Email already registered'
                }), 400

            # Create OTP record
            otp_record = OTP(
                email=email,
                phone=data.get('phone', ''),
                registration_data={}
            )
            db.session.add(otp_record)
            db.session.commit()
            
            # Send email OTP
            email_sent = EmailService.send_otp_email(
                email=email,
                otp=otp_record.email_otp
            )
            
            if not email_sent:
                return jsonify({
                    'error': 'Failed to send email OTP'
                }), 500

            return jsonify({
                'message': 'OTP sent successfully to your email',
                'temp_id': otp_record.id
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Failed to send OTP',
                'message': str(e)
            }), 400

    @staticmethod
    def send_phone_otp(data):
        try:
            phone = data.get('phone')
            temp_id = data.get('temp_id')

            otp_record = OTP.query.get(temp_id)
            if not otp_record:
                return jsonify({'error': 'Please verify email first'}), 400

            # Update phone number and generate new OTP
            otp_record.phone = phone
            otp_record.phone_otp = otp_record.generate_otp()
            otp_record.expires_at = datetime.utcnow() + timedelta(minutes=10)
            
            db.session.commit()
            
            # Send SMS OTP
            sms_sent = SMSService.send_otp_sms(
                phone_number=phone,
                otp=otp_record.phone_otp
            )
            
            if not sms_sent:
                return jsonify({
                    'error': 'Failed to send SMS OTP'
                }), 500

            return jsonify({
                'message': 'OTP sent successfully to your phone'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Failed to send OTP',
                'message': str(e)
            }), 400

    @staticmethod
    def verify_email(data):
        try:
            temp_id = data.get('temp_id')
            email_otp = data.get('email_otp')

            otp_record = OTP.query.get(temp_id)
            
            if not otp_record:
                return jsonify({'error': 'Invalid temporary ID'}), 400
                
            if datetime.utcnow() > otp_record.expires_at:
                return jsonify({'error': 'OTP expired'}), 400

            if email_otp != otp_record.email_otp:
                return jsonify({'error': 'Invalid OTP'}), 400

            otp_record.is_email_verified = True
            db.session.commit()

            return jsonify({
                'message': 'Email verified successfully'
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'Email verification failed',
                'message': str(e)
            }), 400

    @staticmethod
    def verify_phone(data):
        try:
            temp_id = data.get('temp_id')
            phone_otp = data.get('phone_otp')

            otp_record = OTP.query.get(temp_id)
            
            if not otp_record:
                return jsonify({'error': 'Invalid temporary ID'}), 400
                
            if datetime.utcnow() > otp_record.expires_at:
                return jsonify({'error': 'OTP expired'}), 400

            if phone_otp != otp_record.phone_otp:
                return jsonify({'error': 'Invalid OTP'}), 400

            otp_record.is_phone_verified = True
            db.session.commit()

            return jsonify({
                'message': 'Phone number verified successfully'
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'Phone verification failed',
                'message': str(e)
            }), 400

    @staticmethod
    def complete_registration(data):
        try:
            temp_id = data.get('temp_id')
            otp_record = OTP.query.get(temp_id)
            
            if not otp_record:
                return jsonify({'error': 'Invalid temporary ID'}), 400

            if not otp_record.is_email_verified or not otp_record.is_phone_verified:
                return jsonify({
                    'error': 'Both email and phone must be verified',
                    'email_verified': otp_record.is_email_verified,
                    'phone_verified': otp_record.is_phone_verified
                }), 400

            # Create registration
            new_registration = Registration(
                name=data.get('name'),
                email=otp_record.email,
                mobile_number=otp_record.phone,
                requirements=data.get('requirement'),
                technologies=data.get('preferredTechnology')
            )
            
            db.session.add(new_registration)
            db.session.delete(otp_record)
            db.session.commit()

            return jsonify({
                'message': 'Registration successful!',
                'user_id': new_registration.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Registration failed',
                'message': str(e)
            }), 400

    @staticmethod
    def select_winners():
        try:
            winners = Registration.select_winners(3)
            
            if not winners:
                return jsonify({
                    'error': 'No registered users found'
                }), 404

            winners_data = []
            for winner in winners:
                # Send notification email
                EmailService.send_winner_email(
                    email=winner.email,
                    name=winner.name
                )
                
                # Send SMS notification
                SMSService.send_winner_sms(
                    phone_number=f"{winner.country_code}{winner.mobile_number}",
                    name=winner.name
                )
                
                winners_data.append({
                    "name": winner.name,
                    "email": winner.email,
                    "phone": winner.mobile_number
                })

            return jsonify({
                'message': 'Winners selected and notified!',
                'winners': winners_data
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Failed to select winners',
                'message': str(e)
            }), 500

    @staticmethod
    def get_all_users():
        try:
            users = Registration.query.all()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify({
                'error': 'Failed to fetch users',
                'message': str(e)
            }), 500

    @staticmethod
    def initiate_verification(data):
        try:
            # Check if email already exists
            existing_registration = Registration.query.filter_by(email=data.get('email')).first()
            if existing_registration:
                return jsonify({
                    'error': 'Email already registered'
                }), 400

            # Create OTP record with all user data
            otp_record = OTP(data)
            db.session.add(otp_record)
            db.session.commit()
            
            # Send email OTP
            email_sent = EmailService.send_otp_email(
                email=data.get('email'),
                otp=otp_record.email_otp
            )
            
            # Send SMS OTP
            sms_sent = SMSService.send_otp_sms(
                phone_number=f"{data.get('country_code')}{data.get('phone')}",
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

            # Create registration
            new_registration = Registration(
                name=otp_record.name,
                email=otp_record.email,
                country_code=otp_record.country_code,
                mobile_number=otp_record.phone,
                technologies=otp_record.technologies,
                requirements=otp_record.requirements
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