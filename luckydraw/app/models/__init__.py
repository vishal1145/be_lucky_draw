from app.models.registration import Registration
from app.controllers.registration_controller import RegistrationController
from app.models.otp import OTP
from app.models.announcement import Announcement

# Create tables when app starts
def init_db():
    Registration.create_table() 