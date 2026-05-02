from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPoint

class ModernTitleBar(QWidget):
    """
    Custom title bar for frameless windows.
    Handles dragging and close button.
    """
    def __init__(self, parent, title="PomoSlime Settings"):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(40)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 0, 5, 0)
        self.layout.setSpacing(10)
        
        # Title Label
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #cdd6f4; font-weight: bold; font-size: 13px;")
        
        # Close Button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.parent_window.reject) # Default for QDialog
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #cdd6f4;
                font-size: 20px;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #f38ba8;
                color: #11111b;
            }
        """)
        
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addWidget(self.close_btn)
        
        self.setStyleSheet("background-color: #11111b; border-top-left-radius: 12px; border-top-right-radius: 12px;")
        
        self._drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.parent_window.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
