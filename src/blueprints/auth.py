import datetime
from ..services.auth_service import RegistrationService
from ..services.auth_service import LoginService
from flask import Blueprint, render_template, request, redirect


auth_bp = Blueprint('auth', __name__)

@auth_bp.get('/login')
def login_form():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('login.html', current_time=current_time)

@auth_bp.post('/login')
def login():
    login_service = LoginService()
    email = request.form.get('email')
    user_password = request.form.get('user_password')

    if(login_service.login(email, user_password)):
        return redirect('/') #login user and bring to homepage
    else:
        return render_template('login.html') #add error to template for this case?

@auth_bp.get('/register')
def register_form():
    return render_template('register.html')

@auth_bp.post('/register')
def register():
    registration_service = RegistrationService()
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    user_password = request.form.get('user_password')

    if(registration_service.register(user_name, email, user_password)):
        login_service = LoginService()
        if(login_service.login(email, user_password)):
            return redirect('/') #login user and bring to homepage
        else:
            return redirect('/login')
    return render_template('register.html') #add error to template for this case?

    
    