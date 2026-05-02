# Roadmap: PomoSlime

## Overview

PomoSlime sẽ được phát triển qua 3 giai đoạn chính: Thiết lập nền tảng giám sát hệ thống, tích hợp bộ não AI để phản hồi "cà khịa", và cuối cùng là hoàn thiện hệ thống lưu trữ tiến trình/tiến hóa của bé Slime.

## Phases

- [x] **Phase 1: Nền tảng & Giám sát** - Thiết lập UI trong suốt và bộ máy theo dõi ứng dụng foreground.
- [x] **Phase 2: Bộ não AI & Tương tác** - Kết nối Gemini/Groq và hiển thị phản hồi của Pet.
- [x] **Phase 3: Lưu trữ & Tiến hóa** - Triển khai hệ thống điểm Energy, Level và lưu trữ local.
- [x] **Phase 4: Đồ họa & Âm thanh** - Thay thế Emoji bằng ảnh GIF động và thêm hiệu ứng âm thanh.
- [x] **Phase 5: Productivity Features** - Tích hợp Pomodoro Timer, Settings UI và Báo cáo ngày.
- [x] **Phase 6: Contextual Info & UI Polishing** - Nhận diện thời tiết và sửa lỗi hiển thị bóng thoại.

## Phase Details

### Phase 1: Nền tảng & Giám sát
**Goal**: Tạo ra cửa sổ Pet trong suốt và có thể nhận diện chính xác ứng dụng người dùng đang mở.
**Depends on**: Nothing (first phase)
**Requirements**: MON-01, MON-02, MON-03, UI-01, UI-04, UI-05
**Success Criteria**:
  1. Một cửa sổ nhỏ, trong suốt, luôn nổi hiện trên màn hình.
  2. Người dùng có thể dùng chuột kéo Pet đi khắp màn hình.
  3. Console log hiển thị đúng tên process của cửa sổ foreground mỗi 5 giây.
  4. Menu chuột phải hoạt động để thoát ứng dụng.
**Plans**: 2 plans

Plans:
- [x] 01-01: Thiết lập UI PyQt6 (Transparent, Frameless, Drag support).
- [x] 01-02: Triển khai Monitor Engine sử dụng `psutil` và `pywin32`.

### Phase 2: Bộ não AI & Tương tác
**Goal**: Pet bắt đầu biết nói và thay đổi cảm xúc dựa trên hoạt động của người dùng.
**Depends on**: Phase 1
**Requirements**: AI-01, AI-02, AI-03, UI-02, UI-03
**Success Criteria**:
  1. Ứng dụng gửi được context (tên app) lên Gemini/Groq và nhận về JSON.
  2. Pet hiển thị bóng thoại chứa message "cà khịa" từ AI.
  3. Sprite của Pet thay đổi (Vui/Buồn/Giận) tương ứng với status trong JSON.
**Plans**: 2 plans

Plans:
- [x] 02-01: Tích hợp AI Handler (Gemini/Groq API).
- [x] 02-02: Cập nhật UI để hiển thị Speech Bubble và chuyển đổi Sprite.

### Phase 3: Lưu trữ & Tiến hóa
**Goal**: Hệ thống hóa sự tập trung thành điểm số và lưu trữ dữ liệu.
**Depends on**: Phase 2
**Requirements**: DATA-01, DATA-02
**Success Criteria**:
  1. Điểm Energy tăng/giảm đúng theo phản hồi của AI.
  2. Dữ liệu Energy và Level được lưu lại sau khi tắt app.
  3. Pet có thể "tiến hóa" (đổi sang bộ Sprite xịn hơn) khi đạt đủ điểm.
**Plans**: 1 plan

Plans:
- [x] 03-01: Triển khai Data Layer (JSON/SQLite) và Logic tiến hóa.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Nền tảng & Giám sát | 2/2 | Completed | 2026-05-01 |
| 2. Bộ não AI & Tương tác | 2/2 | Completed | 2026-05-01 |
| 3. Lưu trữ & Tiến hóa | 1/1 | Completed | 2026-05-02 |
| 4. Đồ họa & Âm thanh | 2/2 | Completed | 2026-05-02 |
| 5. Productivity Features | 3/3 | Completed | 2026-05-02 |
| 6. Contextual Info & UI Polishing | 2/2 | Completed | 2026-05-02 |


### Phase 4: Đồ họa & Âm thanh

**Goal:** Thay thế các emoji tĩnh bằng ảnh GIF động và tích hợp âm thanh.
**Requirements**: UI-06, UI-07, AUDIO-01
**Depends on:** Phase 3
**Plans:** 2 plans

Plans:
- [x] 04-01: Triển khai QMovie để hiển thị GIF động cho 4 trạng thái cảm xúc.
- [x] 04-02: Tích hợp AudioPlayer sử dụng winsound với các file .wav tùy chỉnh.

### Phase 5: Productivity Features

**Goal:** Biến PomoSlime thành công cụ hỗ trợ làm việc thực thụ.
**Requirements**: PROD-01, PROD-02, UI-08
**Depends on:** Phase 4
**Plans:** 3 plans

Plans:
- [x] 05-01: Xây dựng đồng hồ Pomodoro (25 phút) đếm ngược ngay trên đầu Pet.
- [x] 05-02: Thiết kế cửa sổ Settings UI để quản lý âm thanh và app mapping.
- [x] 05-03: Triển khai tính năng Daily Report tổng hợp thời gian làm việc nhờ AI.

### Phase 6: Contextual Info & UI Polishing

**Goal:** Nâng cấp trí thông minh theo ngữ cảnh và hoàn thiện trải nghiệm UI.
**Requirements**: AI-04, UI-09
**Depends on:** Phase 5
**Plans:** 2 plans

Plans:
- [x] 06-01: Tích hợp thông tin thời tiết (wttr.in) vào lời chào khởi động của AI.
- [x] 06-02: Sửa lỗi hiển thị bóng thoại (dynamic height) để tránh bị cắt chữ.

---
*Roadmap defined: 2026-05-01*
*Last updated: 2026-05-01 after initialization*
