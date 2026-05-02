import os
import json
import winreg
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QCheckBox, QLabel, QListWidget, QPushButton, QInputDialog,
    QComboBox, QFrame, QProgressBar, QApplication
)
from PyQt6.QtCore import Qt, QPoint
from data.save_manager import SaveManager
from .components.modern_title_bar import ModernTitleBar
from .components.modern_message_box import ModernMessageBox

class SettingsWindow(QDialog):
    def __init__(self, save_mgr: SaveManager, parent=None):
        super().__init__(parent)
        self.save_mgr = save_mgr
        
        # Đường dẫn file mapping
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mapping_path = os.path.join(base_dir, "monitor", "app_mapping.json")
        self.app_mapping = self.load_mapping()

        self.setWindowTitle("Cài đặt PomoSlime")
        self.setFixedSize(500, 520) # Tăng chiều cao để không bị chật
        
        # Căn giữa màn hình
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - 500) // 2, (screen.height() - 520) // 2)
        
        # Thiết lập Frameless và Translucent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("""
            QDialog {
                background: transparent;
                color: #cdd6f4;
                border: none;
                font-family: 'Outfit', 'Segoe UI', Arial;
            }
            #MainContainer {
                background-color: rgba(30, 30, 46, 245);
                border: 1px solid rgba(137, 180, 250, 0.4);
                border-radius: 15px;
            }
            QTabWidget::pane {
                border: 1px solid rgba(69, 71, 90, 0.5);
                border-radius: 12px;
                background: rgba(24, 24, 37, 180);
                margin-top: -1px;
            }
            QTabBar::tab {
                background: rgba(49, 50, 68, 150);
                color: #a6adc8;
                padding: 10px 20px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: rgba(24, 24, 37, 180);
                color: #89b4fa;
                border-bottom: 3px solid #89b4fa;
            }
            QTabBar::tab:hover {
                background: rgba(69, 71, 90, 200);
            }
            
            QLabel { color: #cdd6f4; font-size: 13px; font-weight: 500; }
            QCheckBox { color: #cdd6f4; spacing: 8px; font-size: 13px; }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 6px;
                border: 2px solid #45475a;
            }
            QCheckBox::indicator:checked {
                background-color: #89b4fa;
                image: url(none);
            }
            
            QListWidget {
                background-color: rgba(30, 30, 46, 120);
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
                border-radius: 10px;
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
                border: 1px solid rgba(243, 139, 168, 0.5);
                height: 36px;
            }
            QPushButton#danger_btn:hover { 
                background-color: #f38ba8; 
                color: #11111b; 
            }

            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #313244;
                min-height: 20px;
                border-radius: 3px;
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
            ModernMessageBox.warning(self, "Lỗi", f"Không thể lưu app_mapping.json: {e}")

    def _setup_ui(self):
        self.main_container = QFrame(self)
        self.main_container.setObjectName("MainContainer")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_container)

        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(0, 0, 0, 15)
        container_layout.setSpacing(0)

        # Custom Title Bar
        self.title_bar = ModernTitleBar(self, "Cài đặt PomoSlime")
        container_layout.addWidget(self.title_bar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(15, 10, 15, 0)
        container_layout.addLayout(content_layout)

        tabs = QTabWidget()
        content_layout.addWidget(tabs)

        # ---- Tab 1: Chung ----
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(15)
        
        self.sound_checkbox = QCheckBox("Bật hiệu ứng âm thanh (Tiếng Pop / Ting Ting)")
        self.sound_checkbox.setChecked(self.save_mgr.sound_enabled)
        self.sound_checkbox.toggled.connect(self.save_mgr.set_sound_enabled)
        general_layout.addWidget(self.sound_checkbox)
        
        self.startup_checkbox = QCheckBox("Khởi động cùng Windows")
        self.startup_checkbox.setChecked(self.save_mgr.auto_startup)
        self.startup_checkbox.toggled.connect(self._toggle_startup)
        general_layout.addWidget(self.startup_checkbox)
        
        persona_label = QLabel("Cá tính AI của Slime")
        persona_label.setStyleSheet("font-size: 14px; color: #a6e3a1;")
        general_layout.addWidget(persona_label)
        
        self.persona_combo = QComboBox()
        self.persona_combo.addItems(["Tsundere (Cà khịa)", "Motivator (Cổ vũ)", "Kind (Dịu dàng)"])
        current_p = self.save_mgr.personality
        p_map = {"Tsundere": 0, "Motivator": 1, "Kind": 2}
        self.persona_combo.setCurrentIndex(p_map.get(current_p, 0))
        self.persona_combo.currentIndexChanged.connect(self._change_personality)
        self.persona_combo.setStyleSheet("""
            QComboBox { background: #313244; color: #cdd6f4; border-radius: 5px; padding: 5px 10px; border: 1px solid #45475a; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background: #1e1e2e; color: #cdd6f4; selection-background-color: #89b4fa; selection-color: #11111b; border: 1px solid #45475a; outline: none; }
        """)
        general_layout.addWidget(self.persona_combo)
        
        pomo_label = QLabel("Quản lý Pomodoro")
        pomo_label.setStyleSheet("font-size: 15px; color: #fab387; font-weight: bold;")
        general_layout.addWidget(pomo_label)
        
        self.stop_pomo_btn = QPushButton("⏹ Dừng Pomodoro hiện tại")
        self.stop_pomo_btn.setObjectName("danger_btn")
        self.stop_pomo_btn.clicked.connect(self._stop_pomo)
        general_layout.addWidget(self.stop_pomo_btn)
        
        general_layout.addStretch()
        tabs.addTab(general_tab, "Cấu hình chung")

        # ---- Tab 2: Phân loại ----
        app_tab = QWidget()
        app_layout = QVBoxLayout(app_tab)
        lists_layout = QHBoxLayout()
        
        work_col = QVBoxLayout()
        work_col.addWidget(QLabel("Tập trung (Work):"))
        self.work_list = QListWidget()
        self.work_list.addItems(self.app_mapping.get("Work", []))
        work_col.addWidget(self.work_list)
        btn_layout_w = QHBoxLayout()
        btn_add_w = QPushButton("➕")
        btn_add_w.clicked.connect(lambda: self.add_app("Work", self.work_list))
        btn_del_w = QPushButton("❌")
        btn_del_w.clicked.connect(lambda: self.del_app("Work", self.work_list))
        btn_layout_w.addWidget(btn_add_w)
        btn_layout_w.addWidget(btn_del_w)
        work_col.addLayout(btn_layout_w)
        
        dist_col = QVBoxLayout()
        dist_col.addWidget(QLabel("Xao nhãng (Dist):"))
        self.dist_list = QListWidget()
        self.dist_list.addItems(self.app_mapping.get("Distraction", []))
        dist_col.addWidget(self.dist_list)
        btn_layout_d = QHBoxLayout()
        btn_add_d = QPushButton("➕")
        btn_add_d.clicked.connect(lambda: self.add_app("Distraction", self.dist_list))
        btn_del_d = QPushButton("❌")
        btn_del_d.clicked.connect(lambda: self.del_app("Distraction", self.dist_list))
        btn_layout_d.addWidget(btn_add_d)
        btn_layout_d.addWidget(btn_del_d)
        dist_col.addLayout(btn_layout_d)
        
        lists_layout.addLayout(work_col)
        lists_layout.addLayout(dist_col)
        app_layout.addLayout(lists_layout)
        tabs.addTab(app_tab, "Phân loại App")

        # ---- Tab 3: Thống kê ----
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        
        stats = self.save_mgr.time_stats
        work_m = int(stats.get("Work", 0))
        dist_m = int(stats.get("Distraction", 0))
        total = work_m + dist_m if (work_m + dist_m) > 0 else 1
        
        work_bar = QProgressBar()
        work_bar.setValue(int((work_m/total)*100))
        work_bar.setFormat(f"Tập trung: {work_m}m")
        work_bar.setStyleSheet("""
            QProgressBar { border: 1px solid rgba(166, 227, 161, 0.3); border-radius: 12px; text-align: center; height: 36px; background: rgba(30, 30, 46, 100); color: #11111b; font-weight: 800; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #a6e3a1, stop:1 #94e2d5); border-radius: 11px; }
        """)
        stats_layout.addWidget(work_bar)
        
        dist_bar = QProgressBar()
        dist_bar.setValue(int((dist_m/total)*100))
        dist_bar.setFormat(f"Xao nhãng: {dist_m}m")
        dist_bar.setStyleSheet("""
            QProgressBar { border: 1px solid rgba(243, 139, 168, 0.3); border-radius: 12px; text-align: center; height: 36px; background: rgba(30, 30, 46, 100); color: #cdd6f4; font-weight: 800; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f38ba8, stop:1 #fab387); border-radius: 11px; }
        """)
        stats_layout.addWidget(dist_bar)
        stats_layout.addStretch()
        tabs.addTab(stats_tab, "📊 Thống kê")

        close_btn = QPushButton("Hoàn tất")
        close_btn.setObjectName("primary_btn")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        content_layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def _stop_pomo(self):
        if hasattr(self.parent(), "stop_pomodoro"):
            self.parent().stop_pomodoro()
            ModernMessageBox.information(self, "Thông báo", "Đã dừng Pomodoro!")

    def _change_personality(self, index):
        p_list = ["Tsundere", "Motivator", "Kind"]
        self.save_mgr.set_personality(p_list[index])

    def _toggle_startup(self, enabled):
        self.save_mgr.set_auto_startup(enabled)
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "PomoSlime"
        exe_path = f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if enabled: winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                try: winreg.DeleteValue(key, app_name)
                except FileNotFoundError: pass
            winreg.CloseKey(key)
        except Exception as e: ModernMessageBox.warning(self, "Lỗi Registry", str(e))

    def add_app(self, category: str, list_widget: QListWidget):
        name, ok = QInputDialog.getText(self, f"Thêm {category}", "Tên tiến trình:")
        if ok and name.strip():
            self.app_mapping.setdefault(category, []).append(name.strip())
            list_widget.addItem(name.strip())
            self.save_mapping()

    def del_app(self, category: str, list_widget: QListWidget):
        item = list_widget.currentItem()
        if item:
            self.app_mapping[category].remove(item.text())
            list_widget.takeItem(list_widget.row(item))
            self.save_mapping()
