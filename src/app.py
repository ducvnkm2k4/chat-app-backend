from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from src.models import db
import os

# Load biến môi trường từ .env
load_dotenv()

def create_app():
    # Khởi tạo Flask app
    app = Flask(__name__)
    
    # Cấu hình CORS chi tiết hơn
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Cấu hình database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo db với app
    db.init_app(app)

    # Import các blueprint sau khi init db (tránh circular import)
    from src.routes.auth import auth_bp
    from src.routes.chat import chat_bp
    from src.routes.main import main_bp

    # Đăng ký blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(main_bp)

    # Xử lý lỗi
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Tạo tất cả các bảng và default group
    with app.app_context():
        # Import các models
        from src.models.user import User
        from src.models.chat import Message
        
        # Tạo tables
        db.create_all()

    return app

# Tạo app instance
app = create_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Chạy app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
