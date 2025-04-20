from functools import wraps
from flask import request, redirect, url_for, flash, jsonify
import jwt
import os
from datetime import datetime, timedelta
from src.models.user import User

def generate_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

def get_current_user():
    """Get current user from JWT token"""
    token = request.headers.get('Authorization')
    if not token:
        return None
        
    try:
        token = token.split(' ')[1]  # Remove 'Bearer ' prefix
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        return User.query.get(payload['user_id'])
    except:
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function 