from flask_mail import Mail, Message
from flask import render_template_string, render_template

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
                                <p>Best regards,<br>Team Muhandis Market</p>
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
                'Welcome to Lucky Draw! 🎉',
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
                                Welcome to Muhandis Market, the leading platform for freelance Engineers and Architects! 
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
                                <p>Best,<br>Team Muhandis Market</p>
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