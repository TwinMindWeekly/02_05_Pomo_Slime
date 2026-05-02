import json
import os
from datetime import date

class SaveManager:
    """
    Quản lý lưu trữ tiến trình (Energy, Level) vào file JSON cục bộ.
    """
    def __init__(self, save_path: str = None):
        if save_path is None:
            # Lưu ở thư mục app data của user hoặc thư mục hiện tại
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.save_path = os.path.join(base_dir, "save_data.json")
        else:
            self.save_path = save_path

        self.data = {
            "level": 1,
            "energy": 0,
            "max_energy_for_next_level": 100,
            "last_opened_date": "",
            "sound_enabled": True,
            "time_stats": {"Work": 0, "Distraction": 0, "Mixed": 0} # Lưu trữ theo phút
        }
        self.load()

    def register_startup(self) -> bool:
        """
        Kiểm tra xem đây có phải là lần mở app đầu tiên trong ngày không.
        Trả về True nếu là lần đầu trong ngày, False nếu mở lại trong cùng ngày.
        """
        today_str = date.today().isoformat()
        last_opened = self.data.get("last_opened_date", "")
        
        is_first_time = (last_opened != today_str)
        
        if is_first_time:
            self.reset_time_stats() # Khởi tạo lại thống kê cho ngày mới

        # Cập nhật ngày mở mới nhất
        self.data["last_opened_date"] = today_str
        self.save()
        
        return is_first_time

    def load(self):
        """Đọc dữ liệu từ file JSON."""
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Cập nhật các key có sẵn để tránh mất default values nếu file cũ
                    self.data.update(loaded)
            except (json.JSONDecodeError, IOError):
                print("[Data] File save bị lỗi, dùng dữ liệu mặc định.")

    def save(self):
        """Lưu dữ liệu hiện tại xuống file JSON."""
        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"[Data] Lỗi lưu file: {e}")

    def add_energy(self, amount: int) -> bool:
        """
        Cộng/trừ năng lượng. Nếu đạt max_energy, tăng level.
        Trả về True nếu có level up.
        """
        self.data["energy"] += amount
        
        # Không để energy âm
        if self.data["energy"] < 0:
            self.data["energy"] = 0

        level_up = False
        while self.data["energy"] >= self.data["max_energy_for_next_level"]:
            self.data["energy"] -= self.data["max_energy_for_next_level"]
            self.data["level"] += 1
            # Cấp sau cần nhiều năng lượng hơn 20%
            self.data["max_energy_for_next_level"] = int(self.data["max_energy_for_next_level"] * 1.2)
            level_up = True

        self.save()
        return level_up

    @property
    def level(self) -> int:
        return self.data["level"]

    @property
    def energy(self) -> int:
        return self.data["energy"]

    @property
    def max_energy(self) -> int:
        return self.data["max_energy_for_next_level"]

    # ---- Phase 5: Productivity Features ----

    @property
    def sound_enabled(self) -> bool:
        return self.data.get("sound_enabled", True)

    def set_sound_enabled(self, enabled: bool):
        self.data["sound_enabled"] = enabled
        self.save()

    def add_time_stat(self, app_type: str, seconds: int):
        """Cộng thêm thời gian sử dụng vào thống kê trong ngày (quy đổi sang phút)."""
        if "time_stats" not in self.data:
            self.data["time_stats"] = {"Work": 0, "Distraction": 0, "Mixed": 0}
        
        minutes = seconds / 60.0
        if app_type in ["Work", "Distraction", "Mixed"]:
            self.data["time_stats"][app_type] += minutes
            self.save()

    def reset_time_stats(self):
        """Khởi tạo lại thống kê khi qua ngày mới."""
        self.data["time_stats"] = {"Work": 0, "Distraction": 0, "Mixed": 0}
        self.save()

    @property
    def time_stats(self) -> dict:
        return self.data.get("time_stats", {"Work": 0, "Distraction": 0, "Mixed": 0})
