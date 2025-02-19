from flask_mail import Mail, Message
from flask import render_template_string

mail = Mail()

class EmailService:
    @staticmethod
    def send_otp_email(email, otp):
        try:
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
            html = render_template_string(html_content, otp=otp)
            
            # Create message
            msg = Message(
                'Email Verification OTP',
                recipients=[email],
                html=html
            )
            
            # Send email
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False 

    @staticmethod
    def send_winner_email(email, name):
        try:
            html_content = '''
            <html>
                <body>
                    <h2>Congratulations {{ name }}!</h2>
                    <p>You have been selected as a winner in our Lucky Draw!</p>
                    <p>We will contact you shortly with more details.</p>
                    <p>Thank you for participating!</p>
                </body>
            </html>
            '''
            
            html = render_template_string(html_content, name=name)
            
            msg = Message(
                'Congratulations! You Won the Lucky Draw!',
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
            html_content = '''
            <html>
                <body>
                    <h2>Welcome {{ name }}!</h2>
                    <p>Thank you for registering with us.</p>
                    <p>Your registration has been completed successfully.</p>
                </body>
            </html>
            '''
            
            html = render_template_string(html_content, name=name)
            
            msg = Message(
                'Welcome to Our Platform',
                recipients=[email],
                html=html
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error sending welcome email: {str(e)}")
            return False 