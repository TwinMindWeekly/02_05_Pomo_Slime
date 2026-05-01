# Stack Research

**Domain:** AI Desktop Pet / Productivity Tool
**Researched:** 2026-05-01
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.10+ | Core Language | Dễ triển khai, hỗ trợ tốt các thư viện hệ thống và AI. |
| PyQt6 | 6.x | UI Framework | Hỗ trợ tốt các cửa sổ trong suốt (WA_TranslucentBackground) và Frameless windows. |
| psutil | 5.9.x | System Monitoring | Tiêu chuẩn để lấy danh sách tiến trình và tài nguyên hệ thống. |
| pywin32 | latest | Windows API | Cần thiết để lấy handles của cửa sổ foreground trên Windows. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Groq | latest | AI Inference | Khi cần phản hồi "cà khịa" cực nhanh với độ trễ thấp. |
| Google-generativeai| latest | Gemini API | Khi cần phân loại ngữ cảnh phức tạp hoặc xử lý hội thoại dài. |
| SQLite3 | built-in | Data Storage | Lưu trữ điểm Energy, Level và lịch sử tập trung. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| venv | Virtual Environment | Luôn sử dụng venv để quản lý dependencies. |
| pip | Package Manager | Cài đặt các thư viện cần thiết. |

## Installation

```bash
# Core
pip install PyQt6 psutil pywin32

# AI
pip install groq google-generativeai
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| PyQt6 | Tkinter | Nếu muốn cực kỳ nhẹ, nhưng Tkinter khó xử lý transparency chuyên sâu hơn. |
| psutil | os.popen | Không nên dùng vì chậm và khó quản lý hơn. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Electron | Tốn RAM/CPU khủng khiếp cho một Desktop Pet nhỏ. | PyQt6/Python. |
| PySide2 | Đã cũ, nên dùng PyQt6 hoặc PySide6. | PyQt6. |

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| PyQt6 | Python 3.10+ | Đảm bảo hiệu năng ổn định. |
| pywin32 | Windows only | Logic lấy foreground window sẽ khác trên macOS/Linux. |

## Sources

- Official PyQt6 Docs — Window Flags verification.
- Groq/Gemini Documentation — Free tier limits check.
- StackOverflow — Foreground window monitoring patterns.

---
*Stack research for: PomoSlime*
*Researched: 2026-05-01*
