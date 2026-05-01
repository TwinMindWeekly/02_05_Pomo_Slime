# Architecture Research

**Domain:** AI Desktop Pet / Productivity Tool
**Researched:** 2026-05-01
**Confidence:** HIGH

## Proposed Architecture

PomoSlime sẽ hoạt động theo mô hình **Hybrid Event-Polling**:
- **Polling**: Một luồng nền (Background Thread) liên tục kiểm tra cửa sổ foreground mỗi X giây (ví dụ 5s).
- **Event-driven**: UI của PyQt6 cập nhật dựa trên tín hiệu (Signals) từ luồng giám sát.

### Component Diagram

1. **Monitor Engine (Background Thread)**: 
   - Sử dụng `pywin32` lấy foreground window.
   - Sử dụng `psutil` lấy tên process.
   - So khớp với Local Cache (Whitelist/Blacklist).
2. **Brain Handler**:
   - Nhận context từ Monitor.
   - Nếu cần (app mới hoặc đến giờ "cà khịa"), gọi AI API.
   - Phân tích JSON trả về để cập nhật trạng thái.
3. **UI Engine (Main Thread)**:
   - Quản lý cửa sổ trong suốt.
   - Hiển thị Sprite tương ứng với mood.
   - Hiển thị bóng thoại (Speech bubble) chứa message.
4. **Data Persistence**:
   - Lưu trữ điểm số và cấu hình vào file local.

## Technical Patterns

### Transparent Frameless Window (PyQt6)
Sử dụng các flags:
- `Qt.WindowType.FramelessWindowHint`: Bỏ viền.
- `Qt.WindowType.WindowStaysOnTopHint`: Luôn nổi.
- `Qt.WidgetAttribute.WA_TranslucentBackground`: Nền trong suốt.

### Hybrid Classification Logic
1. Kiểm tra `local_mapping.json`.
2. Nếu không thấy -> Gửi lên AI phân loại.
3. Lưu kết quả AI vào `local_mapping.json` để lần sau không cần gọi API nữa.

## Data Schema (Local)

**stats.json**:
```json
{
  "total_energy": 120,
  "level": 2,
  "current_mood": "Happy",
  "last_check": "2026-05-01T19:00:00"
}
```

**mapping.json**:
```json
{
  "code.exe": "Work",
  "facebook.exe": "Distraction",
  "chrome.exe": "Mixed"
}
```

---
*Architecture research for: PomoSlime*
*Researched: 2026-05-01*
