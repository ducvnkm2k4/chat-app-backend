from . import api_bp
from src.utils.response import success_response, error_response

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response({
        'status': 'healthy',
        'message': 'Server is running'
    })

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users endpoint"""
    try:
        # Add your user retrieval logic here
        return success_response({'users': []})
    except Exception as e:
        return error_response(str(e), 500) 