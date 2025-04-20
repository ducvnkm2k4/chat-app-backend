from flask import Blueprint, request
from src.models import db
from src.models.user import User
from src.utils.response import success_response, error_response

auth_bp = Blueprint('auth', __name__)

# API đăng ký
@auth_bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate input
        if not all(k in data for k in ['username', 'email', 'password']):
            return error_response('Missing required fields', 400)
            
        # Create new user without checking existence
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )        
        db.session.add(user)
        db.session.commit()
        
        return success_response({
            'user': user.to_dict()
        }, 'User registered successfully')
        
    except Exception as e:
        return error_response(str(e), 500)

# API đăng nhập
@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate input
        if not all(k in data for k in ['email', 'password']):
            return error_response('Missing required fields', 400)
            
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return error_response('Invalid username or password', 401)
        
        return success_response({
            'user': user.to_dict()
        }, 'Login successful')
        
    except Exception as e:
        return error_response(str(e), 500)
