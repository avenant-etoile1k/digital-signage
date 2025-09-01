from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask import request, redirect, url_for, flash
from .models import User
from passlib.hash import bcrypt
from werkzeug.security import check_password_hash

login_manager = LoginManager()

def hash_password(password):
    return bcrypt.hash(password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def verify_password(user, password):
    return bcrypt.verify(password, user.password_hash)