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

        self.setWindowTitle("⚙️ Cài đặt PomoSlime")
        self.setFixedSize(450, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial;
            }
            QLabel, QCheckBox { color: #cdd6f4; font-size: 13px; }
            QListWidget {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 4px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #b4befe; }
            QTabWidget::pane { border: 1px solid #45475a; border-radius: 4px; }
            QTabBar::tab {
                background: #313244;
                color: #cdd6f4;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { background: #89b4fa; color: #1e1e2e; font-weight: bold; }
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
        
        self.sound_checkbox = QCheckBox("Bật hiệu ứng âm thanh (Tiếng Pop / Ting Ting)")
        self.sound_checkbox.setChecked(self.save_mgr.sound_enabled)
        self.sound_checkbox.toggled.connect(self.save_mgr.set_sound_enabled)
        
        general_layout.addWidget(self.sound_checkbox)
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
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

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
