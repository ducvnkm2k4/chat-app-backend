from flask import Blueprint, request, jsonify
from src.models import db
from src.models.user import User
from src.models.chat import Message
from src.utils.response import success_response, error_response
from src.services.phishing_detector import PhishingDetector

chat_bp = Blueprint('chat', __name__)
phishing_detector = PhishingDetector()

# API lấy tin nhắn
@chat_bp.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        # Lấy các tin nhắn gần đây (ví dụ: 50 tin nhắn mới nhất)
        messages = Message.query.order_by(Message.created_at.desc()).all()

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


# API gửi tin nhắn
import re  # Thêm thư viện regex ở đầu file

# ...

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
        url_pattern = r'https?://[^\s]+'  # regex tìm URL
        urls = re.findall(url_pattern, content)

        # Mặc định là không phải phishing
        is_phishing = False

        # Nếu có URL -> kiểm tra từng URL
        for url in urls:
            if phishing_detector.check_message(url):
                is_phishing = True
                break  # Nếu có 1 URL là phishing thì dừng lại luôn

        # Tạo tin nhắn mới
        message = Message(
            content=content,
            user_id=user.id,
            is_phishing=is_phishing
        )
        
        db.session.add(message)
        db.session.commit()
        
        return success_response({
            'message': message.to_dict(),
            'is_phishing': is_phishing
        }, 'Message sent successfully')
    except Exception as e:
        return error_response(str(e), 500)

