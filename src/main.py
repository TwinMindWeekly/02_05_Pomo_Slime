import sys
import os

# Đảm bảo import hoạt động khi chạy từ thư mục src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.pet_window import PetWindow
from monitor.monitor_engine import MonitorEngine
from brain.brain_handler import BrainHandler


def main():
    """Entry point của PomoSlime."""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Không tắt khi đóng window

    # Khởi tạo cửa sổ Pet
    window = PetWindow()

    # Khởi tạo Brain (đọc API key từ env)
    brain = BrainHandler(
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        gemini_api_key=os.getenv("GEMINI_API_KEY", "")
    )

    # Khởi tạo Monitor Engine
    monitor = MonitorEngine()

    def on_status_changed(process_name: str, app_type: str, window_title: str):
        print(f"[UI Update] {process_name} → {app_type}")
        # Gọi AI để tạo phản hồi
        response = brain.analyze(process_name, app_type, window_title)
        
        if response:
            # Cập nhật UI
            window.update_mood(response.status, response.message)
            print(f"[Slime] {response.status} | {response.message} | Energy: {response.energy_change:+d}")

    # Kết nối tín hiệu
    monitor.status_changed.connect(on_status_changed)
    monitor.start()

    # Hiển thị Pet
    window.show()

    # Dừng monitor sạch sẽ khi thoát
    app.aboutToQuit.connect(monitor.stop)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
