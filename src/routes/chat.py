from flask import Blueprint, request, jsonify, session
from src.models import db
from src.models.user import User
from src.models.chat import Message
from src.utils.response import success_response, error_response
from src.services.phishing_detector import PhishingDetector
from src.utils.auth import login_required
from src.app import socketio
import re
from urllib.parse import urlparse

chat_bp = Blueprint('chat', __name__)
phishing_detector = PhishingDetector()

# Hàm để kiểm tra và thêm scheme nếu không có
def add_scheme_if_missing(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url  # Thêm http:// nếu không có scheme
    return url

@chat_bp.route('/api/messages', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['message', 'userid']):
            return error_response('Missing required fields', 400)
        
        user = User.query.get(data['userid'])
        if not user:
            return error_response('User not found', 404)
        
        content = data['message']
        
        # === Tách URL từ nội dung tin nhắn ===
        url_pattern = r'\b(?:https?://|www\.)[^\s]+|\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'  # regex tìm URL
        urls = re.findall(url_pattern, content)

        # Mặc định là không phải phishing
        is_phishing = False

        # Nếu không có URL theo mẫu regex (có thể là URL không có scheme), kiểm tra và thêm scheme mặc định
        all_urls = []

        # Kiểm tra và thêm scheme nếu thiếu
        for url in urls:
            url_with_scheme = add_scheme_if_missing(url)
            all_urls.append(url_with_scheme)
        print("URLs after adding scheme:", all_urls)
        # Nếu có URL -> kiểm tra từng URL
        for url in all_urls:
            if phishing_detector.check_message(url) == 0:
                is_phishing = True
                break  # Nếu có 1 URL là phishing thì dừng lại luôn
        print("Phishing check result:", is_phishing)
        # Tạo tin nhắn mới
        message = Message(
            content=content,
            user_id=user.id,
            is_phishing=is_phishing
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Chuẩn bị dữ liệu tin nhắn để gửi qua WebSocket
        message_data = {
            'id': message.id,
            'content': message.content,
            'is_phishing': message.is_phishing,
            'user_id': message.user_id,
            'username': user.username,
            'created_at': message.created_at.isoformat(),
            'updated_at': message.updated_at.isoformat()
        }
        
        # Gửi tin nhắn qua WebSocket
        socketio.emit('new_message', message_data)
        
        return success_response({
            'message': message_data,
            'is_phishing': is_phishing
        }, 'Message sent successfully')
    except Exception as e:
        return error_response(str(e), 500)

# API lấy tin nhắn
@chat_bp.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        # Lấy các tin nhắn gần đây (ví dụ: 50 tin nhắn mới nhất)
        messages = Message.query.order_by(Message.created_at.asc()).all()

        # Lấy thông tin mỗi tin nhắn kèm theo tên người gửi
        messages_with_user = [
            {
                'id': message.id,
                'content': message.content,
                'is_phishing': message.is_phishing,
                'user_id': message.user_id,
                'username': message.user.username,  # Lấy tên người gửi từ đối tượng User
                'created_at': message.created_at.isoformat(),
                'updated_at': message.updated_at.isoformat()
            }
            for message in messages
        ]
        
        return success_response({
            'messages': messages_with_user
        })
    except Exception as e:
        return error_response(str(e), 500)
