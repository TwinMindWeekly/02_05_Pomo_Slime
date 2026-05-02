import platform

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

    def play_pop(self):
        """Phát âm thanh pop-up nhẹ nhàng khi bong bóng thoại xuất hiện."""
        if self.is_windows:
            # Phát âm thanh hệ thống mặc định không chặn (Async)
            self.winsound.PlaySound("SystemDefault", self.winsound.SND_ALIAS | self.winsound.SND_ASYNC)

    def play_level_up(self):
        """Phát âm thanh khi Slime tiến hóa / Lên cấp."""
        if self.is_windows:
            # Âm thanh thông báo (thường là tiếng Ting/Chord)
            self.winsound.PlaySound("SystemAsterisk", self.winsound.SND_ALIAS | self.winsound.SND_ASYNC)
