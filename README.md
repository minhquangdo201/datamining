# Ứng Dụng Phân Loại Tin Nhắn Rác

## Giới thiệu
Ứng dụng này bao gồm source code của hai phần: backend và frontend.

- **Thư mục backend**: Bao gồm dữ liệu được lưu trong file `spam.csv`, các mô hình học máy và file `app.py` để chạy máy chủ.
- **Thư mục frontend**: Bao gồm code để chạy giao diện người dùng.

## Hướng dẫn khởi động

**LƯU Ý:**  
Hãy sửa lại các đường dẫn sao cho đúng vì mỗi thiết bị cách đọc đường dẫn sẽ khác nhau nên có thể sẽ lỗi vì sai đường dẫn. Cần cài đặt đầy đủ các thư viện Python cần thiết, cài đặt Node.js và MongoDB.

1. **Bước 1**: Tải trực tiếp hoặc clone project GitHub về máy tính cá nhân.

2. **Bước 2**: Tải tất cả các thư viện Python cần thiết để chạy các file trong thư mục backend. 

3. **Bước 3**: Chạy file `app.py` trong thư mục backend để khởi chạy máy chủ.

4. **Bước 4**: Từ thư mục gốc (datamining) chuyển đến thư mục frontend bằng lệnh `cd frontend`, sau đó gõ lệnh `npm install` để cài đặt các package.

5. **Bước 5**: Sau khi cài đặt xong, gõ lệnh `npm start` để khởi chạy giao diện.

## Cách sử dụng
Ứng dụng bao gồm:
- Một ô input để nhập tin nhắn.
- Select option để chọn mô hình muốn sử dụng.

Cần điền đầy đủ ô tin nhắn và chọn mô hình để có thể kiểm tra.  
Ấn vào dòng chữ "History" để xem lịch sử kiểm tra tin nhắn.
