from PyQt6.QtWidgets import QWidget, QLabel, QMenu, QApplication, QProgressBar
from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QMovie
import os
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
        
        # Movie hiện tại
        self.current_movie = None

        self._setup_window()
        self._setup_ui()
        
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
        
        # ---- Pomodoro Timer Label ----
        self.pomo_label = QLabel("", self)
        self.pomo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pomo_label.setStyleSheet("""
            color: #f38ba8; /* Red */
            font-size: 16px;
            font-weight: bold;
            background: rgba(30, 30, 46, 180);
            border-radius: 8px;
            padding: 2px;
        """)
        self.pomo_label.setGeometry(25, 45, self.WINDOW_WIDTH - 50, 25)
        self.pomo_label.hide()
        
        # Set mặc định là Happy
        self._set_movie(MOOD_SPRITES["Happy"])

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

    def _set_movie(self, gif_path: str):
        """Hàm helper để thay đổi GIF an toàn."""
        if os.path.exists(gif_path):
            movie = QMovie(gif_path)
            self.sprite_label.setMovie(movie)
            movie.start()
            self.current_movie = movie
        else:
            self.sprite_label.setText("O_O") # Fallback nếu file lỗi

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
        # Đổi Animation (nếu có Evolving thì ưu tiên, nếu đang Pomodoro thì giữ nguyên form)
        if self.pomo_seconds_left > 0 and status != "Evolving":
            gif_path = MOOD_SPRITES.get("Evolving") # Dùng form vàng làm Focus Mode
        else:
            gif_path = MOOD_SPRITES.get(status, MOOD_SPRITES["Sad"])
            
        self._set_movie(gif_path)

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

    # ---- Drag Support ----

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
