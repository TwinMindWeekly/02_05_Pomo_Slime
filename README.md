# PomoSlime 🟢

Bé Slime đồng hành giúp bạn duy trì trạng thái Deep Work.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
cd src
python main.py
```

## Cấu trúc dự án

```
src/
├── main.py               # Entry point
├── ui/
│   └── pet_window.py     # Cửa sổ Pet (Transparent, Frameless)
└── monitor/
    ├── monitor_engine.py  # Giám sát foreground window
    └── app_mapping.json   # Danh sách phân loại ứng dụng
assets/
└── sprites/              # Sprite ảnh cho bé Slime (Phase 2)
```
