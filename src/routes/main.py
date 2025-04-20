from flask import Blueprint, jsonify
from src.utils.response import success_response, error_response

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response({
        'status': 'healthy',
        'message': 'Server is running'
    }) 