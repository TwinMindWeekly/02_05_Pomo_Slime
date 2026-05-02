from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from .modern_title_bar import ModernTitleBar

class ModernMessageBox(QDialog):
    """
    Custom premium message box to replace QMessageBox.
    """
    def __init__(self, parent, title, message, icon_type="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(320, 180)

        # Container
        self.main_container = QFrame(self)
        self.main_container.setObjectName("MsgContainer")
        self.main_container.setStyleSheet("""
            #MsgContainer {
                background-color: #1e1e2e;
                border: 1px solid #45475a;
                border-radius: 12px;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_container)

        layout = QVBoxLayout(self.main_container)
        layout.setContentsMargins(0, 0, 0, 15)
        layout.setSpacing(0)

        # Title Bar
        self.title_bar = ModernTitleBar(self, title)
        layout.addWidget(self.title_bar)

        # Content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 15, 20, 10)
        layout.addLayout(content_layout)

        self.msg_label = QLabel(message)
        self.msg_label.setWordWrap(True)
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setStyleSheet("color: #cdd6f4; font-size: 13px; font-weight: 500;")
        content_layout.addWidget(self.msg_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 10, 0, 0)
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFixedSize(80, 32)
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #89b4fa, stop:1 #b4befe);
                color: #11111b;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background: #b4befe; }
        """)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)

    @staticmethod
    def information(parent, title, message):
        dialog = ModernMessageBox(parent, title, message, "info")
        return dialog.exec()

    @staticmethod
    def warning(parent, title, message):
        dialog = ModernMessageBox(parent, title, message, "warning")
        return dialog.exec()
