# PomoSlime 🟢

Bé Slime đồng hành giúp bạn duy trì trạng thái **Deep Work** thông qua sự kết hợp giữa AI và cơ chế Pomodoro.

## Tính năng chính
- **Giám sát thông minh:** Tự động nhận diện ứng dụng bạn đang dùng (Work/Distraction/Mixed).
- **AI "Cà khịa":** Phản hồi hài hước, mỏ hỗn theo phong cách Gen-Z dựa trên hoạt động thực tế.
- **Đồng hồ Pomodoro:** Chế độ tập trung 25 phút với đồng hồ hiển thị ngay trên đầu Pet.
- **Cửa sổ Cài đặt:** Tùy chỉnh danh sách ứng dụng và âm thanh (Pop/Ting) trực tiếp qua giao diện.
- **Báo cáo cuối ngày:** AI tổng kết và chấm điểm mức độ chăm chỉ của bạn.
- **Contextual Greeting:** Chào hỏi thông minh dựa trên thời gian và thời tiết hiện tại.

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```
2. Cấu hình API Key (Groq hoặc Gemini):
```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

## Chạy ứng dụng

```bash
cd src
python main.py
```

## Cấu trúc dự án
- `src/main.py`: Entry point chính của ứng dụng.
- `src/ui/`: Chứa giao diện Pet, Cửa sổ Cài đặt và trình phát âm thanh.
- `src/monitor/`: Bộ máy giám sát cửa sổ foreground.
- `src/brain/`: Xử lý logic AI và hệ thống prompt.
- `src/data/`: Quản lý lưu trữ tiến trình và cài đặt người dùng.
- `assets/`: Chứa các tài nguyên ảnh GIF và âm thanh tùy chỉnh.
- `.planning/`: Hồ sơ quản lý dự án theo chuẩn Get Shit Done (GSD).

## Yêu cầu hệ thống
- Windows (Sử dụng `pywin32` và `winsound`).
- Python 3.10+.
