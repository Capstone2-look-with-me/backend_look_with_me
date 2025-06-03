# Look With Me - Face Recognition API

## Giới thiệu

**Look With Me** là một API nhận diện khuôn mặt sử dụng FastAPI, hỗ trợ giao tiếp thời gian thực qua Socket.IO. Ứng dụng cho phép trích xuất đặc trưng khuôn mặt từ ảnh, nhận diện khuôn mặt dựa trên danh bạ người dùng, và tích hợp dễ dàng với các hệ thống khác.

## Tính năng chính

- Trích xuất encoding khuôn mặt từ ảnh (API REST).
- Nhận diện khuôn mặt theo danh bạ từng người dùng (qua Socket.IO).
- Kết nối với API bên ngoài để lấy danh bạ.
- Hỗ trợ CORS, dễ dàng tích hợp frontend.
- Đóng gói sẵn Docker, dễ deploy.

## Công nghệ sử dụng

- **FastAPI**: Framework API hiện đại, nhanh, dựa trên Python 3.6+, hỗ trợ async/await.
- **Uvicorn**: ASGI server, dùng để chạy ứng dụng FastAPI.
- **face_recognition**: Thư viện nhận diện khuôn mặt dựa trên dlib, sử dụng mô hình deep learning.
- **Socket.IO**: Thư viện hỗ trợ giao tiếp thời gian thực giữa client và server.
- **Pillow (PIL)**: Thư viện xử lý ảnh, dùng để đọc và chuyển đổi ảnh.
- **NumPy**: Thư viện tính toán số học, dùng để xử lý dữ liệu ảnh dạng mảng.
- **python-dotenv**: Quản lý biến môi trường từ file .env.
- **requests**: Thư viện gọi HTTP request, dùng để tương tác với API bên ngoài.
- **Docker**: Công cụ đóng gói ứng dụng, giúp dễ dàng triển khai và chạy trong môi trường container.

## Cài đặt

### Yêu cầu

- Python 3.12+
- pip
- Docker (nếu muốn chạy bằng container)

### Cài đặt thủ công

1. Cài các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```

2. Tạo file `.env` trong thư mục `assets/env/` với biến:
    ```
    API_URL=<địa chỉ API lấy danh bạ>
    ```

3. Chạy ứng dụng:
    ```bash
    python main.py
    ```
    hoặc dùng Uvicorn:
    ```bash
    uvicorn main:app --host=0.0.0.0 --port=8080 --reload
    ```

### Chạy bằng Docker

```bash
docker build -t lookwithme-backend .
docker run -p 8080:8080 --env-file=assets/env/.env lookwithme-backend
```

## Sử dụng

### REST API

- `GET /`  
  Kiểm tra API hoạt động.

- `POST /face_encodings`  
  Trích xuất encoding khuôn mặt từ ảnh.  
  **Body:** file ảnh (multipart/form-data, key: `file`)

### Socket.IO

- **initialize**  
  Gửi userId và access_token để tải danh bạ.

- **recognize_face**  
  Gửi encoding khuôn mặt để nhận diện.

## Cấu trúc thư mục

- `main.py`: Khởi tạo API, định nghĩa endpoint.
- `socket_manager.py`: Quản lý các sự kiện Socket.IO.
- `face_recognition_service.py`: Xử lý logic nhận diện khuôn mặt.
- `api_client.py`: Giao tiếp với API lấy danh bạ.
- `config.py`: Đọc biến môi trường.
- `requirements.txt`: Danh sách thư viện.
- `Dockerfile`: Đóng gói ứng dụng.
- `assets/env/.env`: File cấu hình biến môi trường.

## Ghi chú

- Ứng dụng sử dụng thư viện `face_recognition` (dựa trên dlib), cần cài đặt các thư viện hệ thống như trong Dockerfile.
- Đảm bảo API lấy danh bạ trả về đúng định dạng JSON như mô tả trong code. 