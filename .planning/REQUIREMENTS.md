# Requirements: Focus Spirit

**Defined:** 2026-05-01
**Core Value:** Duy trì sự tập trung của người dùng thông qua sự gắn kết cảm xúc với desktop pet và phản hồi thông minh từ AI.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### MONITOR: System Monitoring

- [ ] **MON-01**: Ứng dụng có thể lấy tên tiến trình của cửa sổ foreground trên Windows.
- [ ] **MON-02**: Tần suất quét hệ thống có thể điều chỉnh (mặc định 5-10 giây).
- [ ] **MON-03**: Có cơ chế phân loại nhanh dựa trên danh sách Whitelist/Blacklist (Local Cache).

### BRAIN: AI Logic & Personality

- [ ] **AI-01**: Tích hợp API Gemini/Groq để xử lý ngôn ngữ tự nhiên.
- [ ] **AI-02**: AI có thể tạo phản hồi JSON với định dạng: status, message, energy_change.
- [ ] **AI-03**: Phản hồi của AI phải súc tích, mang tính cách "High-tech" và "Cà khịa".

### UI: Desktop Pet Interface

- [ ] **UI-01**: Hiển thị cửa sổ trong suốt, không viền (Frameless) và luôn nổi (Always on Top).
- [ ] **UI-02**: Hiển thị hình ảnh (Sprite) của Pet dựa trên trạng thái (Happy/Sad/Angry/Evolving).
- [ ] **UI-03**: Hiển thị bóng thoại (Speech bubble) để hiện thông điệp từ AI.
- [ ] **UI-04**: Cho phép người dùng kéo thả (Drag) vị trí Pet trên màn hình.
- [ ] **UI-05**: Có menu chuột phải (Context Menu) để thoát ứng dụng hoặc bật/tắt Study Mode.

### DATA: Persistence & Progress

- [ ] **DATA-01**: Lưu trữ điểm Energy và Level hiện tại vào file local.
- [ ] **DATA-02**: Lưu trữ danh sách Whitelist/Blacklist ứng dụng đã được phân loại.

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Sound & Animation
- **SND-01**: Hiệu ứng âm thanh khi Pet thay đổi trạng thái.
- **ANI-01**: Animation chuyển động mượt mà hơn cho Sprite.

### Advanced Analytics
- **ANLY-01**: Biểu đồ thống kê thời gian tập trung theo tuần/tháng.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Multi-platform support | Ưu tiên Windows cho máy cá nhân trước. |
| Cloud Sync | Tránh phức tạp về hạ tầng và bảo mật dữ liệu cá nhân. |
| Social Features | Giữ ứng dụng ở mức công cụ tập trung cá nhân. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| MON-01 | Phase 1 | Pending |
| MON-02 | Phase 1 | Pending |
| MON-03 | Phase 1 | Pending |
| UI-01 | Phase 1 | Pending |
| UI-04 | Phase 1 | Pending |
| UI-05 | Phase 1 | Pending |
| AI-01 | Phase 2 | Pending |
| AI-02 | Phase 2 | Pending |
| AI-03 | Phase 2 | Pending |
| UI-02 | Phase 2 | Pending |
| UI-03 | Phase 2 | Pending |
| DATA-01 | Phase 3 | Pending |
| DATA-02 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-01*
*Last updated: 2026-05-01 after initial definition*
