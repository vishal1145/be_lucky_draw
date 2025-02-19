from twilio.rest import Client
from flask import current_app

class SMSService:
    @staticmethod
    def send_otp_sms(phone_number, otp):
        try:
            # For testing: Just print the OTP instead of sending SMS
            print(f"SMS OTP for {phone_number}: {otp}")
            return True  # Always return success for testing
            
            # Uncomment below code when Twilio credentials are ready
            '''
            client = Client(
                current_app.config['TWILIO_ACCOUNT_SID'],
                current_app.config['TWILIO_AUTH_TOKEN']
            )
            
            message = client.messages.create(
                body=f'Your OTP for registration is: {otp}',
                from_=current_app.config['TWILIO_PHONE_NUMBER'],
                to=phone_number
            )
            '''
            
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return True  # Return True even if there's an error for testing

    @staticmethod
    def send_winner_sms(phone_number, name):
        try:
            # For testing: Just print the message instead of sending SMS
            print(f"Winner SMS for {phone_number}: Congratulations {name}! You won!")
            return True
            
            # Uncomment below code when Twilio credentials are ready
            '''
            client = Client(
                current_app.config['TWILIO_ACCOUNT_SID'],
                current_app.config['TWILIO_AUTH_TOKEN']
            )
            
            message = client.messages.create(
                body=f'Congratulations {name}! You have been selected as a winner in our Lucky Draw! We will contact you shortly with more details.',
                from_=current_app.config['TWILIO_PHONE_NUMBER'],
                to=phone_number
            )
            '''
            
        except Exception as e:
            print(f"Error sending winner SMS: {str(e)}")
            return True  # Return True even if there's an error for testing 