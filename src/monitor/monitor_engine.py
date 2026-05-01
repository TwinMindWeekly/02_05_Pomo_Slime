import json
import time
import threading
import os
import psutil
import win32gui
import win32process
from PyQt6.QtCore import QObject, pyqtSignal


class MonitorEngine(QObject):
    """
    Luồng nền giám sát cửa sổ foreground của PomoSlime.

    Chạy mỗi POLL_INTERVAL giây, phát tín hiệu `status_changed`
    khi phát hiện process foreground mới thay đổi.

    Signals:
        status_changed(str, str, str): (tên_process, loại_app, tên_cửa_sổ)
            loại_app: 'Work' | 'Distraction' | 'Mixed' | 'Unknown'
    """

    status_changed = pyqtSignal(str, str, str)

    POLL_INTERVAL = 10  # giây

    def __init__(self, mapping_path: str = None):
        super().__init__()
        self._running = False
        self._thread = None
        self._last_process = ""

        # Tải local mapping từ file JSON
        if mapping_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            mapping_path = os.path.join(base_dir, "app_mapping.json")

        with open(mapping_path, "r", encoding="utf-8") as f:
            self._mapping = json.load(f)

        # Tạo flat lookup dict để tra cứu nhanh O(1): tên_app.lower() → category
        self._app_lookup: dict[str, str] = {}
        for category, apps in self._mapping.items():
            for app in apps:
                self._app_lookup[app.lower()] = category

    # ---- Public API ----

    def start(self):
        """Bắt đầu luồng giám sát nền."""
        self._running = True
        self._thread = threading.Thread(
            target=self._poll_loop,
            daemon=True,
            name="PomoSlime-Monitor"
        )
        self._thread.start()
        print("[Monitor] Bắt đầu giám sát...")

    def stop(self):
        """Dừng luồng giám sát."""
        self._running = False
        print("[Monitor] Đã dừng.")

    def get_current_classification(self, process_name: str) -> str:
        """Truy vấn phân loại tức thì (không cần đợi poll)."""
        return self._classify(process_name)

    # ---- Internal ----

    def _get_foreground_process(self) -> tuple[str, str]:
        """Lấy tên process và tên cửa sổ đang ở foreground trên Windows."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid <= 0:
                return "", ""
            process = psutil.Process(pid)
            return process.name(), window_title
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
            return "", ""

    def _classify(self, process_name: str) -> str:
        """
        Phân loại ứng dụng dựa trên local cache.

        Returns:
            'Work'        — Công việc / học tập
            'Distraction' — Giải trí, mạng xã hội
            'Mixed'       — Trình duyệt (có thể là cả hai)
            'Unknown'     — Chưa có trong danh sách
        """
        return self._app_lookup.get(process_name.lower(), "Unknown")

    def _poll_loop(self):
        """Vòng lặp polling chính chạy trên background thread."""
        while self._running:
            process_name, window_title = self._get_foreground_process()

            # Chỉ phát tín hiệu khi process thực sự thay đổi
            if process_name and process_name != self._last_process:
                self._last_process = process_name
                app_type = self._classify(process_name)
                print(f"[Monitor] {process_name} → {app_type} | {window_title[:50]}")
                self.status_changed.emit(process_name, app_type, window_title)

            time.sleep(self.POLL_INTERVAL)
