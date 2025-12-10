from flask import render_template_string, render_template, current_app
import logging
import traceback
from app.services.emailjs_service import EmailJSService

# Setup logger
logger = logging.getLogger(__name__)

class EmailService:
    """
    Email service wrapper - uses EmailJS only
    Maintains backward compatibility with existing code
    """
    @staticmethod
    def send_otp_email(email, otp):
        """
        Send OTP via email using EmailJS
        Returns: True if successful, False otherwise
        """
        try:
            logger.info(f"[EMAIL] Sending OTP email to: {email}")
            return EmailJSService.send_otp_email(email, otp)
        except Exception as e:
            logger.error(f"[EMAIL] Exception in send_otp_email: {str(e)}")
            return False 

    @staticmethod
    def send_winner_email(email, name):
        """
        Send winner notification email using EmailJS
        Returns: True if successful, False otherwise
        """
        try:
            logger.info(f"[EMAIL] Attempting to send winner email to: {email}")
            logger.info(f"[EMAIL] Winner name: {name}")
            return EmailJSService.send_winner_email(email, name)
        except Exception as e:
            logger.error(f"[EMAIL] Exception in send_winner_email: {str(e)}")
            return False 

    @staticmethod
    def send_welcome_email(email, name, first_name=None, announcement_date=None):
        """
        Send welcome email using EmailJS
        """
        try:
            logger.info(f"[EMAIL] ===== Starting welcome email send =====")
            logger.info(f"[EMAIL] Recipient: {email}")
            logger.info(f"[EMAIL] Name: {name}")
            logger.info(f"[EMAIL] First Name: {first_name or name}")
            
            result = EmailJSService.send_welcome_email(email, name, first_name, announcement_date)
            
            if result:
                logger.info(f"[EMAIL] ✅ Welcome email sent successfully")
            else:
                logger.error(f"[EMAIL] ❌ Welcome email failed to send")
            
            logger.info(f"[EMAIL] ===== Welcome email send completed =====")
            return result
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Exception in send_welcome_email: {str(e)}")
            import traceback
            logger.error(f"[EMAIL] Traceback: {traceback.format_exc()}")
            return False

    @staticmethod
    def send_verification_email(email, name, verification_link):
        """
        Send email verification link using EmailJS
        """
        try:
            logger.info(f"[EMAIL] Sending verification email to: {email}")
            return EmailJSService.send_verification_email(email, name, verification_link)
        except Exception as e:
            logger.error(f"[EMAIL] Exception in send_verification_email: {str(e)}")
            return False 
            return False 