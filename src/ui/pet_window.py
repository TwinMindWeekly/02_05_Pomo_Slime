from PyQt6.QtWidgets import QWidget, QLabel, QMenu, QApplication
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QAction


# Sprite map theo trạng thái cảm xúc (emoji placeholder)
# Phase 3 sẽ thay bằng ảnh PNG thật của bé Slime
MOOD_SPRITES = {
    "Happy":    "🟢",   # Xanh lá — vui vẻ, đang tập trung tốt
    "Sad":      "🔵",   # Xanh dương — buồn, nhớ nhà
    "Angry":    "🔴",   # Đỏ — tức vì bị xao nhãng
    "Evolving": "🌟",   # Sao vàng — đang tiến hóa!
}


class PetWindow(QWidget):
    """
    Cửa sổ chính của PomoSlime.
    - Frameless + Transparent + Always on Top + Draggable
    - Hiển thị Sprite emoji theo mood
    - Hiển thị Speech Bubble với message từ AI (tự ẩn sau 8 giây)
    """

    WINDOW_SIZE = 150  # pixels

    def __init__(self):
        super().__init__()
        self._drag_pos = QPoint()
        self._hide_timer = None
        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        """Thiết lập các thuộc tính cốt lõi của cửa sổ."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool  # Ẩn khỏi Taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WINDOW_SIZE, self.WINDOW_SIZE)

        # Vị trí mặc định: góc dưới bên phải màn hình
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.width() - self.WINDOW_SIZE - 20,
            screen.height() - self.WINDOW_SIZE - 60
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
        self.bubble_label.setGeometry(0, -70, self.WINDOW_SIZE, 65)
        self.bubble_label.hide()  # Ẩn ban đầu

        # ---- Sprite / Emoji Label ----
        self.sprite_label = QLabel(MOOD_SPRITES["Happy"], self)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setStyleSheet("font-size: 80px; background: transparent;")
        self.sprite_label.setGeometry(0, 0, self.WINDOW_SIZE, self.WINDOW_SIZE)

    # ---- Public: Update từ AI ----

    def update_mood(self, status: str, message: str):
        """
        Cập nhật Sprite và hiển thị Speech Bubble với message từ AI.
        Bubble tự ẩn sau 8 giây.

        Args:
            status: 'Happy' | 'Sad' | 'Angry' | 'Evolving'
            message: Câu thoại từ BrainHandler
        """
        # Đổi Sprite
        emoji = MOOD_SPRITES.get(status, MOOD_SPRITES["Sad"])
        self.sprite_label.setText(emoji)

        # Hiển thị Speech Bubble
        if message:
            self.bubble_label.setText(message)
            self.bubble_label.show()

            # Reset và bắt đầu timer tự ẩn (8 giây)
            if self._hide_timer is not None:
                self._hide_timer.stop()
            self._hide_timer = QTimer(self)
            self._hide_timer.setSingleShot(True)
            self._hide_timer.timeout.connect(self.bubble_label.hide)
            self._hide_timer.start(8000)

    # ---- Drag Support ----

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

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

        quit_action = QAction("❌ Thoát PomoSlime", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        menu.exec(event.globalPos())
