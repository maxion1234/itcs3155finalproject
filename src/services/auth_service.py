from flask import Flask, render_template
from ..repositories.app_user_repository import AppUserRepository
import re
#from ..models import AppUser uncomment once this import error is fixed
from security import bcrypt

class RegistrationService:

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def register(self, user_name, email, user_password):
        app_user_repository = AppUserRepository()

        if user_name == '' or email == '' or user_password == '':
            return False #different error?

        #check email is valid and not taken
        if not re.fullmatch(self.regex, email):
            return False
        
        if app_user_repository.get_user_by_email(email) is not None:
            return False

        #hash password, check length first?
        hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')

        app_user_repository.create_app_user(user_name, email, hashed_password)

        return True
        
class LoginService:

    def login(self, email, entered_password):
        app_user_repository = AppUserRepository()

        if email == '' or entered_password == '':
            return False
        
        app_user = app_user_repository.get_user_by_email(email)

        if app_user is None:
            return False

        if not bcrypt.check_password_hash(app_user.user_password, entered_password):
            return False
        
        #TO DO - save user in session using cookies
        #could be done here or in another class below - possibly implement JWTs

        return True
        
        
        
