import sys
import os

# Đảm bảo import hoạt động khi chạy từ thư mục src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.pet_window import PetWindow
from monitor.monitor_engine import MonitorEngine
from brain.brain_handler import BrainHandler
from data.save_manager import SaveManager

def get_weather() -> str:
    """Lấy thông tin thời tiết hiện tại qua wttr.in."""
    import urllib.request
    try:
        req = urllib.request.Request("https://wttr.in/?format=%C+%t", headers={'User-Agent': 'curl/7.68.0'})
        return urllib.request.urlopen(req, timeout=2).read().decode('utf-8').strip()
    except Exception:
        return "Không rõ thời tiết"

def main():
    """Entry point của PomoSlime."""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Không tắt khi đóng window

    # Khởi tạo Brain (đọc API key từ env)
    brain = BrainHandler(
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        gemini_api_key=os.getenv("GEMINI_API_KEY", "")
    )

    # Khởi tạo Data Layer
    save_mgr = SaveManager()

    # Khởi tạo cửa sổ Pet
    window = PetWindow(save_mgr=save_mgr, brain=brain)
    
    # Cập nhật UI ban đầu
    window.update_stats(save_mgr.level, save_mgr.energy, save_mgr.max_energy)

    # Gửi lời chào khởi động kèm thời tiết
    weather = get_weather()
    is_first_time = save_mgr.register_startup()
    startup_title = f"Lần đầu trong ngày. Thời tiết: {weather}" if is_first_time else f"Mở lại trong ngày. Thời tiết: {weather}"
    
    startup_response = brain.analyze("PomoSlime", "Startup", startup_title)
    if startup_response:
        window.update_mood(startup_response.status, startup_response.message, save_mgr.sound_enabled)

    # Khởi tạo Monitor Engine
    monitor = MonitorEngine()

    def on_status_changed(process_name: str, app_type: str, window_title: str):
        print(f"[UI Update] {process_name} → {app_type}")
        
        # Cập nhật thời gian sử dụng (Monitor poll mỗi 10s)
        save_mgr.add_time_stat(app_type, 10)
        
        # Kiểm tra trạng thái Pomodoro
        is_pomo = window.pomo_seconds_left > 0
        
        # Gọi AI để tạo phản hồi
        response = brain.analyze(
            process_name=process_name, 
            app_type=app_type, 
            window_title=window_title,
            is_pomodoro=is_pomo
        )
        
        if response:
            # Cập nhật điểm
            level_up = save_mgr.add_energy(response.energy_change)

            # Cập nhật UI
            if level_up:
                window.update_mood("Evolving", "Tui vừa tiến hóa nè! Đỉnh quá Tính ơi!", save_mgr.sound_enabled)
            else:
                window.update_mood(response.status, response.message, save_mgr.sound_enabled)
            
            window.update_stats(save_mgr.level, save_mgr.energy, save_mgr.max_energy)
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
