# PomoSlime

## What This Is

PomoSlime là một ứng dụng desktop pet thông minh với nhân vật chính là một chú Slime dễ thương. Nó đóng vai trò là một "Thực thể tập trung" sống trong máy tính của người dùng (tên là "Tính"). Nhiệm vụ của nó là giám sát các tiến trình đang chạy và điều chỉnh hành vi, tâm trạng của mình để giúp người dùng duy trì trạng thái "Deep Work" thông qua các tương tác vui nhộn, thông minh và "cà khịa" tinh tế.

## Core Value

Duy trì sự tập trung của người dùng thông qua sự gắn kết cảm xúc với desktop pet và phản hồi thông minh từ AI.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Giám sát tiến trình đang hoạt động (Foreground Window) sử dụng `psutil`.
- [ ] Phân loại ứng dụng thành "Work/Study" hoặc "Distraction" (Hybrid: Local mapping + AI context).
- [ ] Hiển thị Desktop Pet (PyQt6) với cửa sổ trong suốt, luôn nổi (Always on Top).
- [ ] Các trạng thái cảm xúc của Pet: Happy, Sad, Angry, Evolving (đổi Sprite/Icon).
- [ ] AI (Gemini/Groq) tạo phản hồi JSON gồm: status, message, energy_change.
- [ ] Hệ thống tích lũy Energy và tiến hóa (Lưu trữ local qua SQLite hoặc JSON).
- [ ] Cơ chế "Study Mode" toggle để người dùng xác nhận các ứng dụng "vùng xám" (như Browser).

### Out of Scope

- Hỗ trợ đa nền tảng phức tạp (Ưu tiên chạy tốt trên máy cá nhân Windows trước).
- Tính năng đồng bộ hóa cloud hoặc mạng xã hội.
- Các animation 3D phức tạp (Giữ ở mức 2D Sprite tối giản).

## Context

Dự án bắt đầu như một công cụ hỗ trợ cá nhân để giải quyết vấn đề lướt web vô định và mất tập trung khi làm việc/học tập. Người dùng muốn một người đồng hành có tính cách "High-tech", súc tích nhưng thẳng thắn.

## Constraints

- **Tech Stack**: Python 3.10+, PyQt6 (UI), psutil (System info).
- **AI API**: Gemini hoặc Groq (Xử lý ngôn ngữ tự nhiên).
- **Performance**: Phải tiêu tốn ít tài nguyên CPU/RAM để không ảnh hưởng đến công việc chính.
- **Privacy**: Hạn chế gửi dữ liệu nhạy cảm, chỉ gửi tên ứng dụng và ngữ cảnh cần thiết lên AI.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hybrid Classification | Giảm chi phí API và tăng tốc độ phản hồi cho các app quen thuộc. | — Pending |
| PyQt6 Minimalist UI | Dễ triển khai cửa sổ trong suốt và luôn nổi trên desktop. | — Pending |
| AI Personality: Witty/Candid | Tạo sự thú vị và tác động tâm lý mạnh hơn là những lời nhắc nhở khô khan. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-01 after initialization*
