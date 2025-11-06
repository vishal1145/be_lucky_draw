from twilio.rest import Client
from flask import current_app
import logging
from datetime import datetime

# Setup logger
logger = logging.getLogger(__name__)

class SMSService:
    @staticmethod
    def send_otp_sms(phone_number, otp):
        """
        Send OTP via SMS using Twilio or print in test mode
        Returns: True if successful, False otherwise
        """
        try:
            logger.info(f"[SMS] Attempting to send OTP SMS to {phone_number}")
            logger.info(f"[SMS] OTP: {otp}")
            
            # Check if Twilio credentials are configured
            twilio_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
            twilio_token = current_app.config.get('TWILIO_AUTH_TOKEN')
            twilio_phone = current_app.config.get('TWILIO_PHONE_NUMBER')
            
            # If Twilio credentials are available, send actual SMS
            if twilio_sid and twilio_token and twilio_phone:
                logger.info(f"[SMS] Twilio credentials found. Sending SMS via Twilio...")
                try:
                    client = Client(twilio_sid, twilio_token)
                    message = client.messages.create(
                        body=f'Your OTP for registration is: {otp}',
                        from_=twilio_phone,
                        to=phone_number
                    )
                    logger.info(f"[SMS] ✅ SMS sent successfully via Twilio!")
                    return True
                except Exception as twilio_error:
                    logger.error(f"[SMS] Error type: {type(twilio_error).__name__}")
                    return False
            else:
                # Test mode: Just print the OTP instead of sending SMS
                print(f"[SMS TEST MODE] OTP for {phone_number}: {otp}")
                return True  # Return True for testing
            
        except Exception as e:
            logger.error(f"[SMS] ❌ Unexpected error in send_otp_sms: {str(e)}")
            logger.error(f"[SMS] Error type: {type(e).__name__}")
            import traceback
            logger.error(f"[SMS] Traceback: {traceback.format_exc()}")
            return False

    @staticmethod
    def send_winner_sms(phone_number, name):
        """
        Send winner notification via SMS using Twilio or print in test mode
        Returns: True if successful, False otherwise
        """
        try:
            logger.info(f"[SMS] Attempting to send winner SMS to {phone_number}")
            logger.info(f"[SMS] Winner: {name}")
            
            # Check if Twilio credentials are configured
            twilio_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
            twilio_token = current_app.config.get('TWILIO_AUTH_TOKEN')
            twilio_phone = current_app.config.get('TWILIO_PHONE_NUMBER')
            
            # If Twilio credentials are available, send actual SMS
            if twilio_sid and twilio_token and twilio_phone:
                logger.info(f"[SMS] Twilio credentials found. Sending winner SMS via Twilio...")
                try:
                    client = Client(twilio_sid, twilio_token)
                    message_body = f'Congratulations {name}! You have been selected as a winner in our Lucky Draw! We will contact you shortly with more details.'
                    message = client.messages.create(
                        body=message_body,
                        from_=twilio_phone,
                        to=phone_number
                    )
                    logger.info(f"[SMS] ✅ Winner SMS sent successfully via Twilio!")
                    logger.info(f"[SMS] Message SID: {message.sid}")
                    logger.info(f"[SMS] Status: {message.status}")
                    logger.info(f"[SMS] To: {phone_number}")
                    logger.info(f"[SMS] From: {twilio_phone}")
                    logger.info(f"[SMS] Winner: {name}")
                    return True
                except Exception as twilio_error:
                    logger.error(f"[SMS] ❌ Failed to send winner SMS via Twilio: {str(twilio_error)}")
                    logger.error(f"[SMS] Error type: {type(twilio_error).__name__}")
                    return False
            else:
                # Test mode: Just print the message instead of sending SMS
                logger.warning(f"[SMS] ⚠️  TEST MODE: Twilio credentials not configured")
                logger.warning(f"[SMS] Would send winner notification to {phone_number} for {name}")
                logger.warning(f"[SMS] To enable actual SMS, add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER to .env")
                print(f"[SMS TEST MODE] Winner SMS for {phone_number}: Congratulations {name}! You won!")
                return True  # Return True for testing
            
        except Exception as e:
            logger.error(f"[SMS] ❌ Unexpected error in send_winner_sms: {str(e)}")
            logger.error(f"[SMS] Error type: {type(e).__name__}")
            import traceback
            logger.error(f"[SMS] Traceback: {traceback.format_exc()}")
            return False 