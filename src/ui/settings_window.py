import os
import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QCheckBox, QLabel, QListWidget, QPushButton, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from data.save_manager import SaveManager

class SettingsWindow(QDialog):
    def __init__(self, save_mgr: SaveManager, parent=None):
        super().__init__(parent)
        self.save_mgr = save_mgr
        
        # Đường dẫn file mapping
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mapping_path = os.path.join(base_dir, "monitor", "app_mapping.json")
        self.app_mapping = self.load_mapping()

        self.setWindowTitle("Cài đặt PomoSlime")
        self.setFixedSize(480, 420)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Outfit', 'Segoe UI', Arial;
            }
            QTabWidget::pane {
                border: 1px solid #45475a;
                border-radius: 12px;
                background: #181825;
                margin-top: -1px;
            }
            QTabBar::tab {
                background: #313244;
                color: #a6adc8;
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #181825;
                color: #89b4fa;
                border-bottom: 2px solid #89b4fa;
            }
            QTabBar::tab:hover {
                background: #45475a;
            }
            
            QLabel { color: #cdd6f4; font-size: 13px; font-weight: 500; }
            QCheckBox { color: #cdd6f4; spacing: 8px; font-size: 13px; }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #45475a;
            }
            QCheckBox::indicator:checked {
                background-color: #89b4fa;
                image: url(none); /* Có thể thêm icon check nếu muốn */
            }
            
            QListWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 10px;
                padding: 5px;
                outline: none;
            }
            QListWidget::item { padding: 8px; border-radius: 6px; }
            QListWidget::item:selected { background-color: #313244; color: #89b4fa; }
            QListWidget::item:hover { background-color: #313244; }

            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: bold;
                border: 1px solid #45475a;
            }
            QPushButton:hover { background-color: #45475a; border: 1px solid #585b70; }
            
            QPushButton#primary_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #89b4fa, stop:1 #b4befe);
                color: #11111b;
                border: none;
            }
            QPushButton#primary_btn:hover { background: #b4befe; }
            
            QPushButton#danger_btn {
                background-color: rgba(243, 139, 168, 0.1);
                color: #f38ba8;
                border: 1px solid #f38ba8;
            }
            QPushButton#danger_btn:hover { background-color: #f38ba8; color: #11111b; }

            QScrollBar:vertical {
                border: none;
                background: #181825;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #313244;
                min-height: 20px;
                border-radius: 4px;
            }
        """)

        self._setup_ui()

    def load_mapping(self):
        if os.path.exists(self.mapping_path):
            try:
                with open(self.mapping_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"Work": [], "Distraction": [], "Mixed": []}

    def save_mapping(self):
        try:
            with open(self.mapping_path, "w", encoding="utf-8") as f:
                json.dump(self.app_mapping, f, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể lưu app_mapping.json: {e}")

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        # ---- Tab 1: Chung ----
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(15)
        
        self.sound_checkbox = QCheckBox("Bật hiệu ứng âm thanh (Tiếng Pop / Ting Ting)")
        self.sound_checkbox.setChecked(self.save_mgr.sound_enabled)
        self.sound_checkbox.toggled.connect(self.save_mgr.set_sound_enabled)
        general_layout.addWidget(self.sound_checkbox)
        
        general_layout.addSpacing(20)
        
        pomo_label = QLabel("Quản lý Pomodoro")
        pomo_label.setStyleSheet("font-size: 15px; color: #fab387; font-weight: bold;")
        general_layout.addWidget(pomo_label)
        
        self.stop_pomo_btn = QPushButton("⏹ Dừng Pomodoro hiện tại")
        self.stop_pomo_btn.setObjectName("danger_btn")
        self.stop_pomo_btn.clicked.connect(self._stop_pomo)
        general_layout.addWidget(self.stop_pomo_btn)
        
        desc = QLabel("Dừng đếm ngược và đưa Slime về trạng thái bình thường.")
        desc.setStyleSheet("color: #7f849c; font-size: 11px;")
        general_layout.addWidget(desc)
        
        general_layout.addStretch()
        tabs.addTab(general_tab, "Cấu hình chung")

        # ---- Tab 2: Phân loại Ứng dụng ----
        app_tab = QWidget()
        app_layout = QVBoxLayout(app_tab)

        lists_layout = QHBoxLayout()
        
        # Cột Work
        work_col = QVBoxLayout()
        work_col.addWidget(QLabel("Tập trung (Work):"))
        self.work_list = QListWidget()
        self.work_list.addItems(self.app_mapping.get("Work", []))
        work_col.addWidget(self.work_list)
        
        btn_add_work = QPushButton("➕ Thêm")
        btn_add_work.clicked.connect(lambda: self.add_app("Work", self.work_list))
        btn_del_work = QPushButton("❌ Xóa")
        btn_del_work.clicked.connect(lambda: self.del_app("Work", self.work_list))
        
        btn_layout_w = QHBoxLayout()
        btn_layout_w.addWidget(btn_add_work)
        btn_layout_w.addWidget(btn_del_work)
        work_col.addLayout(btn_layout_w)
        
        # Cột Distraction
        dist_col = QVBoxLayout()
        dist_col.addWidget(QLabel("Xao nhãng (Distraction):"))
        self.dist_list = QListWidget()
        self.dist_list.addItems(self.app_mapping.get("Distraction", []))
        dist_col.addWidget(self.dist_list)
        
        btn_add_dist = QPushButton("➕ Thêm")
        btn_add_dist.clicked.connect(lambda: self.add_app("Distraction", self.dist_list))
        btn_del_dist = QPushButton("❌ Xóa")
        btn_del_dist.clicked.connect(lambda: self.del_app("Distraction", self.dist_list))
        
        btn_layout_d = QHBoxLayout()
        btn_layout_d.addWidget(btn_add_dist)
        btn_layout_d.addWidget(btn_del_dist)
        dist_col.addLayout(btn_layout_d)

        lists_layout.addLayout(work_col)
        lists_layout.addLayout(dist_col)
        app_layout.addLayout(lists_layout)

        tabs.addTab(app_tab, "Phân loại Ứng dụng")

        # Nút Đóng
        close_btn = QPushButton("Hoàn tất")
        close_btn.setObjectName("primary_btn")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def _stop_pomo(self):
        """Yêu cầu PetWindow dừng Pomodoro."""
        if hasattr(self.parent(), "stop_pomodoro"):
            self.parent().stop_pomodoro()
            QMessageBox.information(self, "Thông báo", "Đã dừng Pomodoro!")
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể truy cập bộ đếm Pomodoro.")

    def add_app(self, category: str, list_widget: QListWidget):
        app_name, ok = QInputDialog.getText(self, f"Thêm {category}", "Nhập tên tiến trình (VD: notepad.exe):")
        if ok and app_name.strip():
            app_name = app_name.strip()
            if app_name not in self.app_mapping.get(category, []):
                self.app_mapping.setdefault(category, []).append(app_name)
                list_widget.addItem(app_name)
                self.save_mapping()

    def del_app(self, category: str, list_widget: QListWidget):
        selected = list_widget.currentItem()
        if selected:
            app_name = selected.text()
            if app_name in self.app_mapping.get(category, []):
                self.app_mapping[category].remove(app_name)
                list_widget.takeItem(list_widget.row(selected))
                self.save_mapping()
