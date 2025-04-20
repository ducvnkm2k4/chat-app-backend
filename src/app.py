from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from src.models import db
import os

# Load biến môi trường từ .env
load_dotenv()

# Khởi tạo SocketIO
socketio = SocketIO()

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
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Khởi tạo db với app
    db.init_app(app)

    # Khởi tạo SocketIO với app
    socketio.init_app(app, cors_allowed_origins="*")

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

    # Tạo tất cả các bảng
    with app.app_context():
        # Import các models
        from src.models.user import User
        from src.models.chat import Message
        
        # Tạo tables
        db.create_all()

    # WebSocket events
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('message')
    def handle_message(data):
        message = data.get('message')
        if message:
            # Broadcast message to all connected clients
            emit('message', message, broadcast=True)

    return app

# Tạo app instance
app = create_app()

# Chạy app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
