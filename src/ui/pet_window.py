from PyQt6.QtWidgets import QWidget, QLabel, QMenu, QApplication
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction


class PetWindow(QWidget):
    """
    Cửa sổ chính của PomoSlime.
    - Frameless: Không có viền hay thanh tiêu đề.
    - Transparent: Nền trong suốt.
    - Always on Top: Luôn hiện phía trên các cửa sổ khác.
    - Draggable: Người dùng có thể kéo thả.
    """

    WINDOW_SIZE = 150  # pixels

    def __init__(self):
        super().__init__()
        self._drag_pos = QPoint()
        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        """Thiết lập các thuộc tính cốt lõi của cửa sổ."""
        # Xóa viền và làm nền trong suốt
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool  # Ẩn khỏi Taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WINDOW_SIZE, self.WINDOW_SIZE)

        # Đặt vị trí mặc định: góc dưới bên phải màn hình
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.width() - self.WINDOW_SIZE - 20,
            screen.height() - self.WINDOW_SIZE - 60
        )

    def _setup_ui(self):
        """Thiết lập các thành phần UI bên trong cửa sổ."""
        # Placeholder cho Sprite (sẽ thay bằng ảnh thật ở Phase 2)
        self.sprite_label = QLabel("🟢", self)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setStyleSheet("font-size: 80px;")
        self.sprite_label.setGeometry(0, 0, self.WINDOW_SIZE, self.WINDOW_SIZE)

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
