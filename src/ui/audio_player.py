import platform
import os

# Đường dẫn tuyệt đối tới thư mục assets/sounds
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

class AudioPlayer:
    """
    Quản lý phát âm thanh cơ bản cho PomoSlime.
    Sử dụng winsound (chỉ hoạt động trên Windows) để tránh cài đặt thêm dependency nặng.
    """
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        if self.is_windows:
            import winsound
            self.winsound = winsound

    def play_pop(self, enabled: bool = True):
        """Phát âm thanh pop-up nhẹ nhàng khi bong bóng thoại xuất hiện."""
        if self.is_windows and enabled:
            wav_path = os.path.join(SOUNDS_DIR, "pop.wav")
            if os.path.exists(wav_path):
                self.winsound.PlaySound(wav_path, self.winsound.SND_FILENAME | self.winsound.SND_ASYNC)
            else:
                self.winsound.PlaySound("SystemDefault", self.winsound.SND_ALIAS | self.winsound.SND_ASYNC)

    def play_level_up(self, enabled: bool = True):
        """Phát âm thanh khi Slime tiến hóa / Lên cấp."""
        if self.is_windows and enabled:
            wav_path = os.path.join(SOUNDS_DIR, "levelup.wav")
            if os.path.exists(wav_path):
                self.winsound.PlaySound(wav_path, self.winsound.SND_FILENAME | self.winsound.SND_ASYNC)
            else:
                self.winsound.PlaySound("SystemAsterisk", self.winsound.SND_ALIAS | self.winsound.SND_ASYNC)
