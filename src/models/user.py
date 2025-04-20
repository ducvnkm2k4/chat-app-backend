from datetime import datetime
from src.models import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Giữ password đã được băm
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password):
        """So sánh mật khẩu đã băm với mật khẩu gửi từ client."""
        return self.password == password  # Mật khẩu đã được băm ở phía client

    def to_dict(self):
        """Chuyển đổi đối tượng người dùng thành dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'password': self.password  
        }
