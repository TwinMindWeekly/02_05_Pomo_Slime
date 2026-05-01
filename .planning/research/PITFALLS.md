# Pitfalls Research

**Domain:** AI Desktop Pet / Productivity Tool
**Researched:** 2026-05-01
**Confidence:** HIGH

## Known Risks & Mitigation

### 1. Hiệu năng & Tài nguyên (CPU/RAM)
- **Risk**: Polling liên tục hoặc AI xử lý quá nặng làm máy lag.
- **Mitigation**: Chỉ poll mỗi 5-10 giây. Sử dụng các model AI nhỏ/nhanh (Flash/Groq). Tránh dùng các framework nặng như Electron.

### 2. Tương tác chuột (Mouse Passthrough)
- **Risk**: Pet che mất phần mềm khác và người dùng không thể click vào bên dưới.
- **Mitigation**: PyQt6 cho phép set `Qt.WidgetAttribute.WA_TransparentForMouseEvents` khi không cần tương tác, hoặc thiết kế Pet ở vị trí ít bị chạm.

### 3. API Rate Limits (Free Tier)
- **Risk**: Gọi API quá nhiều dẫn đến bị block (429 Error).
- **Mitigation**: Triển khai Local Cache triệt để. Chỉ gọi AI khi thực sự cần câu thoại mới hoặc app mới.

### 4. Quyền riêng tư (Privacy)
- **Risk**: Người dùng e ngại việc bị theo dõi tiến trình.
- **Mitigation**: Chỉ xử lý local tên process. Chỉ gửi context tối giản (App name + Mood) lên AI.

### 5. Tính ổn định của cửa sổ Frameless
- **Risk**: Cửa sổ frameless khó di chuyển hoặc bị lỗi hiển thị trên một số bản Windows.
- **Mitigation**: Cài đặt mouse drag events thủ công. Kiểm tra transparency flags kỹ trên Windows 10/11.

---
*Pitfalls research for: PomoSlime*
*Researched: 2026-05-01*
