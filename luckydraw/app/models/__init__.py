from app.models.registration import Registration
from app.controllers.registration_controller import RegistrationController

# Create tables when app starts
def init_db():
    Registration.create_table() 