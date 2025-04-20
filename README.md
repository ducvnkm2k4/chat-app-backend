# BTL Khai phá dữ liệu và máy học trong an toàn hệ thống

# Giới thiệu
Dự án này tập trung vào việc phát triển một hệ thống chat với khả năng phát hiện URL lừa đảo (phishing) sử dụng máy học. Hệ thống bao gồm backend xử lý API và tích hợp mô hình máy học để phân tích tin nhắn.

# Cấu trúc dự án
```
backend_chat_app/
├── src/
│   ├── models/         # Các model database
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic và ML models
│   ├── static/         # Static files (CSS, JS)
│   ├── templates/      # HTML templates
│   └── utils/          # Utility functions
├── requirements.txt    # Python dependencies
└── .env               # Environment variables
```

# API Documentation

## Authentication
- POST `/api/login`
  - Đăng nhập người dùng
  - Request body: `{ "username": string, "password": string }`
  - Response: `{ "token": string, "user": object }`

- POST `/api/register`
  - Đăng ký người dùng mới
  - Request body: `{ "username": string, "password": string, "email": string }`
  - Response: `{ "message": string, "user": object }`

## Chat
- POST `/api/messages`
  - Gửi tin nhắn mới
  - Request body: `{ "message": string, "userid": number }`
  - Response: `{ "message": object, "is_phishing": boolean }`

- GET `/api/messages`
  - Lấy danh sách tin nhắn
  - Response: `{ "messages": array }`

# WebSocket Events
- `connect`: Kết nối WebSocket
- `disconnect`: Ngắt kết nối WebSocket
- `message`: Nhận tin nhắn mới
- `new_message`: Broadcast tin nhắn mới đến tất cả client

# Tính năng chính
1. Authentication
   - Đăng ký/đăng nhập người dùng

2. Real-time Chat
   - WebSocket cho giao tiếp real-time
   - Broadcast tin nhắn đến tất cả người dùng

3. Phishing Detection
   - Phát hiện URL lừa đảo trong tin nhắn
   - Sử dụng mô hình máy học để phân tích

# Báo cáo
client: https://github.com/ducvnkm2k4/chat_app.git
máy học: https://github.com/ducvnkm2k4/btl_dmml_net.git
báo cáo nghiên cứu: https://docs.google.com/document/d/1omlw5fgTNDKg2MKwOU_6PcMlskKjncK8jpQO8l9orgg/edit?tab=t.0

# Backend
- Flask framework
- SQLAlchemy ORM
- Flask-SocketIO cho real-time communication

# Máy học
- Mô hình phát hiện phishing URL
- Xử lý và phân tích URL
- Tích hợp với hệ thống chat

