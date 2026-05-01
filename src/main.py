import sys
import os

# Đảm bảo import hoạt động khi chạy từ thư mục src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.pet_window import PetWindow
from monitor.monitor_engine import MonitorEngine


def on_status_changed(process_name: str, app_type: str, window_title: str):
    """
    Callback khi Monitor phát hiện thay đổi foreground app.
    Phase 1: Chỉ log ra console.
    Phase 2: Sẽ gọi AI handler để tạo phản hồi.
    """
    print(f"[UI Update] Process: {process_name} | Type: {app_type}")
    # TODO Phase 2: brain_handler.analyze(process_name, app_type, window_title)


def main():
    """Entry point của PomoSlime."""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Không tắt khi đóng window

    # Khởi tạo cửa sổ Pet
    window = PetWindow()

    # Khởi tạo Monitor Engine và kết nối tín hiệu
    monitor = MonitorEngine()
    monitor.status_changed.connect(on_status_changed)
    monitor.start()

    # Hiển thị Pet
    window.show()

    # Dừng monitor sạch sẽ khi thoát
    app.aboutToQuit.connect(monitor.stop)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
