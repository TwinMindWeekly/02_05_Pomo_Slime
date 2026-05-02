from PyQt6.QtWidgets import QWidget, QLabel, QMenu, QApplication, QProgressBar
from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal, QRect
from PyQt6.QtGui import QAction, QMovie, QPixmap, QPainter
import os
import win32api
from ui.audio_player import AudioPlayer
from ui.settings_window import SettingsWindow


# Lấy đường dẫn tuyệt đối tới thư mục assets/sprites
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPRITE_DIR = os.path.join(BASE_DIR, "assets", "sprites")

MOOD_SPRITES = {
    "Happy":    os.path.join(SPRITE_DIR, "happy.gif"),
    "Sad":      os.path.join(SPRITE_DIR, "sad.gif"),
    "Angry":    os.path.join(SPRITE_DIR, "angry.gif"),
    "Evolving": os.path.join(SPRITE_DIR, "evolving.gif"),
}

# Cấu hình Sprite Sheet mới (1024x1024, 4x4 grid)
SPRITE_SHEET_PATH = os.path.join(SPRITE_DIR, "slime_sheet.png")
ANIMATION_CONFIG = {
    "Idle":     {"row": 0, "frames": 4},
    "Work":     {"row": 1, "frames": 4},
    "Break":    {"row": 2, "frames": 4},
    "Sleep":    {"row": 3, "frames": 4},
}


class PetWindow(QWidget):
    """
    Cửa sổ chính của PomoSlime.
    - Frameless + Transparent + Always on Top + Draggable
    - Hiển thị Sprite emoji theo mood
    - Hiển thị Speech Bubble với message từ AI (tự ẩn sau 8 giây)
    """

    WINDOW_WIDTH = 150   # pixels
    WINDOW_HEIGHT = 260  # Tăng lên để chứa bóng thoại dài hơn

    # Tín hiệu nội bộ để xử lý cập nhật giao diện từ luồng nền (Thread-safe)
    mood_updated = pyqtSignal(str, str, bool)
    stats_updated = pyqtSignal(int, int, int)
    pomodoro_ticked = pyqtSignal(int)

    def __init__(self, save_mgr=None, brain=None):
        super().__init__()
        self.save_mgr = save_mgr
        self.brain = brain
        
        self._drag_pos = QPoint()
        self._hide_timer = None
        
        # Biến đếm Pomodoro
        self.pomo_seconds_left = 0
        self.pomo_timer = QTimer(self)
        self.pomo_timer.timeout.connect(self._on_pomo_tick)
        
        # Khởi tạo Audio Player
        self.audio = AudioPlayer()
        
        # Khởi tạo Sprite Animation
        self.sprite_sheet = QPixmap(SPRITE_SHEET_PATH)
        self.current_anim = "Idle"
        self.current_frame = 0
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._update_animation)
        
        # Biến điều khiển nhịp điệu animation
        self._idle_wait_timer = QTimer(self)
        self._idle_wait_timer.setSingleShot(True)
        self._idle_wait_timer.timeout.connect(lambda: self.anim_timer.start())
        
        # Hẹn giờ kiểm tra Idle (Sleep mode)
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self._check_system_idle)

        self._setup_window()
        self._setup_ui()
        
        # Bắt đầu animation và idle timer sau khi UI đã sẵn sàng
        self.anim_timer.start(100) # 10 FPS
        self.idle_timer.start(10000)
        
        # Kết nối tín hiệu
        self.mood_updated.connect(self._do_update_mood)
        self.stats_updated.connect(self._do_update_stats)

    def _setup_window(self):
        """Thiết lập các thuộc tính cốt lõi của cửa sổ."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool  # Ẩn khỏi Taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Vị trí mặc định: góc dưới bên phải màn hình
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.width() - self.WINDOW_WIDTH - 20,
            screen.height() - self.WINDOW_HEIGHT - 60
        )

    def _setup_ui(self):
        """Thiết lập Speech Bubble và Sprite Label."""

        # ---- Speech Bubble (hiện phía trên Sprite) ----
        self.bubble_label = QLabel("", self)
        self.bubble_label.setWordWrap(True)
        self.bubble_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bubble_label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 30, 46, 220);
                color: #cdd6f4;
                border: 1px solid #89b4fa;
                border-radius: 10px;
                padding: 6px 10px;
                font-family: 'Segoe UI', Arial;
                font-size: 11px;
                font-weight: 500;
            }
        """)
        self.bubble_label.setGeometry(0, 0, self.WINDOW_WIDTH, 80) # Tăng chiều cao mặc định
        self.bubble_label.hide()  # Ẩn ban đầu

        # ---- Sprite / Animation Label ----
        self.sprite_label = QLabel(self)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setStyleSheet("background: transparent;")
        self.sprite_label.setGeometry(0, 70, self.WINDOW_WIDTH, self.WINDOW_WIDTH)
        
        # ---- Pomodoro Timer Label (Di chuyển xuống dưới để không đè bóng thoại) ----
        self.pomo_label = QLabel("", self)
        self.pomo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pomo_label.setStyleSheet("""
            color: #f38ba8; /* Red */
            font-size: 14px;
            font-weight: bold;
            background: rgba(30, 30, 46, 150);
            border-radius: 5px;
        """)
        self.pomo_label.setGeometry(40, self.WINDOW_HEIGHT - 70, self.WINDOW_WIDTH - 80, 20)
        self.pomo_label.hide()
        
        # Hiển thị frame đầu tiên
        self._update_animation()

        # ---- Energy Bar ----
        self.energy_bar = QProgressBar(self)
        self.energy_bar.setGeometry(10, self.WINDOW_HEIGHT - 20, self.WINDOW_WIDTH - 20, 10)
        self.energy_bar.setTextVisible(False)
        self.energy_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #45475a;
                border-radius: 5px;
                background-color: #1e1e2e;
            }
            QProgressBar::chunk {
                background-color: #a6e3a1; /* Xanh lá */
                border-radius: 4px;
            }
        """)

        # ---- Level Label ----
        self.level_label = QLabel("Lv.1", self)
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_label.setStyleSheet("color: #f9e2af; font-weight: bold; font-size: 12px; background: transparent;")
        self.level_label.setGeometry(0, self.WINDOW_HEIGHT - 45, self.WINDOW_WIDTH, 20)

    def _update_animation(self):
        """Cắt và hiển thị frame hiện tại từ Sprite Sheet."""
        if not hasattr(self, 'sprite_label') or self.sprite_sheet.isNull():
            return

        config = ANIMATION_CONFIG.get(self.current_anim, ANIMATION_CONFIG["Idle"])
        row = config["row"]
        max_frames = config["frames"]
        
        # Kích thước frame (giả sử 256x256 từ 1024x1024 sheet)
        frame_size = 256
        x = self.current_frame * frame_size
        y = row * frame_size
        
        # Cắt frame
        target_pixmap = self.sprite_sheet.copy(QRect(x, y, frame_size, frame_size))
        # Scale về kích thước UI
        scaled_pixmap = target_pixmap.scaled(
            self.WINDOW_WIDTH, self.WINDOW_WIDTH, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.sprite_label.setPixmap(scaled_pixmap)
        
        # Chuyển frame tiếp theo
        next_frame = self.current_frame + 1
        
        # Logic đặc biệt cho Idle (Nhún xong nghỉ 30s)
        if self.current_anim == "Idle" and next_frame >= max_frames:
            self.current_frame = 0
            self.anim_timer.stop()
            self._idle_wait_timer.start(30000) # Nghỉ 30s
            return

        # Logic đặc biệt cho Sleep (Dừng ở frame cuối)
        if self.current_anim == "Sleep" and next_frame >= max_frames:
            self.current_frame = max_frames - 1 # Giữ ở frame cuối
            self.anim_timer.stop()
            return

        self.current_frame = next_frame % max_frames

    def _set_anim(self, state: str):
        """Thay đổi trạng thái animation."""
        if state in ANIMATION_CONFIG and self.current_anim != state:
            self.current_anim = state
            self.current_frame = 0
            self._idle_wait_timer.stop()
            if not self.anim_timer.isActive():
                self.anim_timer.start()

    # ---- Public: Update từ AI ----

    def update_stats(self, level: int, energy: int, max_energy: int):
        """Phát tín hiệu cập nhật stats (Thread-safe)."""
        self.stats_updated.emit(level, energy, max_energy)

    def update_mood(self, status: str, message: str, sound_enabled: bool = True):
        """Phát tín hiệu cập nhật mood (Thread-safe)."""
        self.mood_updated.emit(status, message, sound_enabled)

    def _do_update_stats(self, level: int, energy: int, max_energy: int):
        """Logic cập nhật thanh năng lượng và cấp độ (Chạy trên Main Thread)."""
        self.level_label.setText(f"Lv.{level}")
        self.energy_bar.setMaximum(max_energy)
        self.energy_bar.setValue(energy)

    def _do_update_mood(self, status: str, message: str, sound_enabled: bool):
        """
        Cập nhật Sprite và hiển thị Speech Bubble.
        Chạy trên Main Thread.
        """
        # Đổi Animation theo trạng thái
        if self.pomo_seconds_left > 0:
            self._set_anim("Work")
        elif status == "Happy":
            self._set_anim("Break")
        elif status == "Sleep":
            self._set_anim("Sleep")
        else:
            self._set_anim("Idle")

        # Hiển thị Speech Bubble
        if message:
            self.bubble_label.setText(message)
            self.bubble_label.setFixedWidth(self.WINDOW_WIDTH)
            self.bubble_label.adjustSize()
            
            # Căn chỉnh lại vị trí để luôn nằm trên đầu Slime
            # (adjustSize có thể làm nó hẹp lại nếu text ngắn, nên ta set lại width)
            new_height = self.bubble_label.height()
            self.bubble_label.setGeometry(0, 70 - new_height - 5, self.WINDOW_WIDTH, new_height)
            
            self.bubble_label.show()
            
            # Phát âm thanh pop
            if status == "Evolving":
                self.audio.play_level_up(sound_enabled)
            else:
                self.audio.play_pop(sound_enabled)

            # Reset và bắt đầu timer tự ẩn (5 giây)
            if self._hide_timer is not None:
                self._hide_timer.stop()
            self._hide_timer = QTimer(self)
            self._hide_timer.setSingleShot(True)
            self._hide_timer.timeout.connect(self.bubble_label.hide)
            self._hide_timer.start(5000)

    def _check_system_idle(self):
        """Kiểm tra thời gian rảnh của hệ thống để chuyển sang trạng thái Sleep."""
        if self.pomo_seconds_left > 0:
            return # Đang focus thì không ngủ

        # Tính thời gian idle (milliseconds)
        millis = win32api.GetTickCount() - win32api.GetLastInputInfo()
        idle_seconds = millis / 1000
        
        if idle_seconds > 60: # 1 phút không chạm máy
            if self.current_anim != "Sleep":
                self._set_anim("Sleep")
                self.update_mood("Sleep", "Khò khò... Tính đi đâu rồi? 💤", False)
        elif self.current_anim == "Sleep":
            # Nếu vừa thức dậy
            self.update_mood("Happy", "A! Tính đã quay lại! Chào mừng bạn! ✨", True)
            self._set_anim("Break")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Ghi nhận vị trí kéo thả
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Nếu người dùng chỉ click (không di chuyển chuột nhiều), coi đó là vuốt ve
            if hasattr(self, '_drag_pos'):
                current_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                # Khoảng cách giữa lúc nhấn và nhả rất nhỏ => Click
                if (current_pos - self._drag_pos).manhattanLength() < 5:
                    self.update_mood("Happy", "Hihi, Tính vuốt ve bé kìa! 🟢", True)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    # ---- Context Menu (Right-click) ----

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item:selected {
                background-color: #313244;
                border-radius: 4px;
            }
        """)

        # Bắt đầu Pomodoro
        pomo_action = QAction("⏱ Bắt đầu Pomodoro (25 phút)", self)
        pomo_action.triggered.connect(self.start_pomodoro)
        menu.addAction(pomo_action)

        # Cài đặt
        settings_action = QAction("⚙️ Cài đặt", self)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)
        
        # Báo cáo ngày
        report_action = QAction("📊 Báo cáo cuối ngày", self)
        report_action.triggered.connect(self.show_daily_report)
        menu.addAction(report_action)
        
        menu.addSeparator()

        quit_action = QAction("❌ Thoát PomoSlime", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        menu.exec(event.globalPos())

    # ---- Phase 5: Productivity Logic ----

    def open_settings(self):
        if self.save_mgr:
            dialog = SettingsWindow(self.save_mgr, self)
            dialog.exec()

    def start_pomodoro(self):
        self.pomo_seconds_left = 25 * 60  # 25 phút
        self.pomo_label.show()
        self.pomo_timer.start(1000)
        self.update_mood("Evolving", "Vào chế độ Focus Mode! Cháy lên Tính ơi!", True)
        self._set_anim("Work")

    def stop_pomodoro(self):
        """Dừng Pomodoro thủ công."""
        self.pomo_seconds_left = 0
        self.pomo_timer.stop()
        self.pomo_label.hide()
        self._set_anim("Idle")
        self.update_mood("Happy", "Đã dừng Pomodoro. Nghỉ ngơi xíu nhé!", True)

    def _on_pomo_tick(self):
        self.pomo_seconds_left -= 1
        mins = self.pomo_seconds_left // 60
        secs = self.pomo_seconds_left % 60
        self.pomo_label.setText(f"{mins:02d}:{secs:02d}")
        
        if self.pomo_seconds_left <= 0:
            self.pomo_timer.stop()
            self.pomo_label.hide()
            self.update_mood("Happy", "Hết giờ Pomodoro rồi! Bạn giỏi lắm, nghỉ xíu đi!", True)

    def show_daily_report(self):
        if not self.save_mgr or not self.brain:
            return
            
        stats = self.save_mgr.time_stats
        w_time = int(stats.get("Work", 0))
        d_time = int(stats.get("Distraction", 0))
        
        self.update_mood("Happy", "Đang tổng hợp báo cáo ngày...", False)
        
        # Gửi dữ liệu thô cho AI tự viết nhận xét (Chạy trên một thread tạm để tránh đơ app? Tạm thời gọi đồng bộ)
        QTimer.singleShot(100, lambda: self._fetch_report(w_time, d_time))

    def _fetch_report(self, w_time: int, d_time: int):
        info_str = f"Work: {w_time} phút, Distraction: {d_time} phút"
        resp = self.brain.analyze("PomoSlime", "Report", info_str)
        if resp:
            # Hiện bubble cực lâu cho báo cáo (15 giây)
            self._do_update_mood(resp.status, resp.message, self.save_mgr.sound_enabled)
            if self._hide_timer:
                self._hide_timer.start(15000)
