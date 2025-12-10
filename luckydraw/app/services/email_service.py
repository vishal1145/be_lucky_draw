from flask_mail import Mail, Message
from flask import render_template_string, render_template, current_app
import logging
import traceback

# Setup logger
logger = logging.getLogger(__name__)

mail = Mail()

class EmailService:
    @staticmethod
    def send_otp_email(email, otp):
        """
        Send OTP via email
        Returns: True if successful, False otherwise
        """
        try:
            # Check if email configuration is available
            mail_server = current_app.config.get('MAIL_SERVER')
            mail_username = current_app.config.get('MAIL_USERNAME')
            
            if not mail_server or not mail_username:
                return True  # Return True for testing
            
            # Email template
            html_content = '''
            <html>
                <body>
                    <h2>Email Verification</h2>
                    <p>Your OTP for registration is: <strong>{{ otp }}</strong></p>
                    <p>This OTP will expire in 10 minutes.</p>
                </body>
            </html>
            '''
            
            # Render template with OTP
            try:
                html = render_template_string(html_content, otp=otp)
            except Exception as template_error:
                logger.error(f"[EMAIL] Failed to render email template: {str(template_error)}")
                raise
            
            # Create message
            try:
                msg = Message(
                    'Email Verification OTP',
                    recipients=[email],
                    html=html
                )
            except Exception as msg_error:
                logger.error(f"[EMAIL] Failed to create email message: {str(msg_error)}")
                raise
            
            # Send email
            try:
                mail.send(msg)
                return True
            except Exception as send_error:
                logger.error(f"[EMAIL] Failed to send email: {str(send_error)}")
                return False
            
        except Exception as e:
            logger.error(f"[EMAIL] Exception in send_otp_email: {str(e)}")
            return False 

    @staticmethod
    def send_winner_email(email, name):
        """
        Send winner notification email
        Returns: True if successful, False otherwise
        """
        try:
            logger.info(f"[EMAIL] Attempting to send winner email to: {email}")
            logger.info(f"[EMAIL] Winner name: {name}")
            
            # Check if email configuration is available
            mail_server = current_app.config.get('MAIL_SERVER')
            mail_username = current_app.config.get('MAIL_USERNAME')
            
            if not mail_server or not mail_username:
                logger.warning(f"[EMAIL] ⚠️  Email configuration not found")
                logger.warning(f"[EMAIL] Winner email would be sent to: {email} for: {name}")
                return True  # Return True for testing
            
            logger.info("[EMAIL] Preparing winner email template...")
            html_content = '''
            <html>
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .email-container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f8f9fc;
                        }
                        .header {
                            text-align: center;
                            color: #6c63ff;
                            margin-bottom: 20px;
                        }
                        .content {
                            background-color: white;
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .welcome-text {
                            font-size: 24px;
                            color: #6c63ff;
                            margin-bottom: 15px;
                            text-align: center;
                        }
                        .activate-button {
                            display: block;
                            width: fit-content;
                            margin: 25px auto;
                            padding: 12px 30px;
                            background-color: #6c63ff;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            font-weight: bold;
                            text-align: center;
                        }
                        .message {
                            text-align: center;
                            margin: 20px 0;
                            color: #555;
                        }
                        .footer {
                            text-align: center;
                            margin-top: 20px;
                            color: #666;
                            font-size: 14px;
                        }
                        .verification-link {
                            word-break: break-all;
                            color: #6c63ff;
                            text-decoration: none;
                        }
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="content">
                            <div class="header">
                                <div class="welcome-text">Congratulations {{ name }}! 🎉</div>
                                <h2>You're a Winner!</h2>
                            </div>
                            
                            <div class="message">
                                You have been selected as a winner in our Lucky Draw!
                            </div>
                            
                            <div class="message">
                                We will contact you shortly with more details about your prize and how to claim it.
                            </div>
                            
                            <div class="message">
                                Thank you for participating in our Lucky Draw!
                            </div>
                            
                            <div class="footer">
                                <p>Best regards,<br>Team Algofolks</p>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            '''
            
            html = render_template_string(html_content, name=name)
            
            msg = Message(
                'Congratulations! You Won the Lucky Draw! 🎉',
                recipients=[email],
                html=html
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error sending winner email: {str(e)}")
            return False 

    @staticmethod
    def send_welcome_email(email, name):
        try:
            # Render the HTML template
            html = render_template('emails/welcome_email.html', name=name)
            
            msg = Message(
                '🎉 Welcome to the Lucky Draw – Your Chance to Win Big!',
                recipients=[email],
                html=html
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error sending welcome email: {str(e)}")
            return False

    @staticmethod
    def send_verification_email(email, name, verification_link):
        try:
            html_content = '''
            <html>
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .email-container {
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f8f9fc;
                        }
                        .header {
                            text-align: center;
                            color: #6c63ff;
                            margin-bottom: 20px;
                        }
                        .content {
                            background-color: white;
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .welcome-text {
                            font-size: 24px;
                            color: #6c63ff;
                            margin-bottom: 15px;
                            text-align: center;
                        }
                        .activate-button {
                            display: block;
                            width: fit-content;
                            margin: 25px auto;
                            padding: 12px 30px;
                            background-color: #6c63ff;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            font-weight: bold;
                            text-align: center;
                        }
                        .message {
                            text-align: center;
                            margin: 20px 0;
                            color: #555;
                        }
                        .footer {
                            text-align: center;
                            margin-top: 20px;
                            color: #666;
                            font-size: 14px;
                        }
                        .verification-link {
                            word-break: break-all;
                            color: #6c63ff;
                            text-decoration: none;
                        }
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="content">
                            <div class="header">
                                <div class="welcome-text">Hi {{ name }}</div>
                                <h2>Activate Your Account</h2>
                            </div>
                            
                            <div class="message">
                                Welcome to Algofolks , the leading platform for freelance Engineers and Architects! 
                                We're excited to have you join our community.
                            </div>
                            
                            <div class="message">
                                To complete your registration, please verify your email by clicking the link below:
                            </div>
                            
                            <a href="{{ verification_link }}" class="activate-button">
                                Verify Email
                            </a>
                            
                            <div class="message">
                                If the button doesn't work, you can copy and paste this link in your browser:
                                <br><br>
                                <a href="{{ verification_link }}" class="verification-link">{{ verification_link }}</a>
                            </div>
                            
                            <div class="message">
                                Thank you for joining us! We're here to support your journey
                            </div>
                            
                            <div class="footer">
                                <p>Best,<br>Team Algofolks </p>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            '''
            
            html = render_template_string(html_content, 
                                        name=name, 
                                        verification_link=verification_link)
            
            msg = Message(
                'Activate Your Account',
                recipients=[email],
                html=html
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error sending verification email: {str(e)}")
            return False 