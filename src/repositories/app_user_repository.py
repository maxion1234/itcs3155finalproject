#from ..models import AppUser uncomment once this import error is fixed
from extensions import db

class AppUserRepository:

    def get_app_user_by_id(self, user_id):
        app_user = AppUser.query.get(user_id)

        return app_user
    
    def create_app_user(self, user_name, email, user_password):
        new_app_user = AppUser(user_name=user_name, email=email, user_password=user_password)

        db.session.add(new_app_user)
        db.session.commit()
        
        return new_app_user
    
    def get_user_by_email(self, email):
        app_user = AppUser.query.filter_by(email=email).first()
        return app_user
    
    