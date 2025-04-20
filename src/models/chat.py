from datetime import datetime
from src.models import db  # hoặc từ flask_sqlalchemy import SQLAlchemy nếu bạn dùng trực tiếp

# === Message model ===
class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_phishing = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Liên kết user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Quan hệ
    user = db.relationship('User', backref='messages')

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'is_phishing': self.is_phishing,
            'user_id': self.user_id,
            'username': self.user.username,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
