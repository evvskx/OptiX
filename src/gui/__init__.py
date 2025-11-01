from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QProgressBar, QStackedWidget, QHBoxLayout
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, Signal, QThread
from PySide6.QtGui import QFont
from src.jobs import jobs
from src.runner import Runner
import winreg, os, time, random


class Worker(QThread):
    progress_signal = Signal(int, int, str)

    def run(self):
        total_tasks = sum(len(job) for job in jobs)
        current_task = 0

        for job in jobs:
            for category, command in job.items():
                self.progress_signal.emit(current_task, total_tasks, f"{category}...")
                Runner().run(command)
                current_task += 1

        self.progress_signal.emit(total_tasks, total_tasks, "Optimization Complete!")


class Title(QWidget):
    def __init__(self, parent=None, bg_color="#202020", text_color="white"):
        super().__init__(parent)
        self.parent = parent
        self.bg_color = bg_color
        self.text_color = text_color
        self.setFixedHeight(32)
        self.setStyleSheet(f"background-color: {bg_color};")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(0)
        self.title = QLabel("")
        font = QFont("Segoe UI", 9)
        self.title.setFont(font)
        self.title.setStyleSheet(f"color: {text_color};")
        layout.addWidget(self.title)
        layout.addStretch()
        self.min_btn = QPushButton("─")
        self.min_btn.setFixedSize(46, 32)
        self.min_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; 
                color: {text_color}; 
                font-size: 10px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.08);
            }}
        """)
        self.min_btn.clicked.connect(self.minimize)
        layout.addWidget(self.min_btn)
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(46, 32)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; 
                color: {text_color}; 
                font-size: 10px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #C42B1C;
                color: white;
            }}
        """)
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)
        self.startPos = None
        self.isDragging = False

    def minimize(self):
        self.parent.showMinimized()

    def close(self):
        self.parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPosition().toPoint()
            self.isDragging = True

    def mouseMoveEvent(self, event):
        if self.isDragging:
            delta = event.globalPosition().toPoint() - self.startPos
            self.parent.move(self.parent.pos() + delta)
            self.startPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.isDragging = False


class GUI(QMainWindow):
    def is_dark_mode(self):
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except Exception:
            return False

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OptiX")
        self.setFixedSize(600, 420)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dark = self.is_dark_mode()
        if self.dark:
            self.bg_color = "#202020"
            self.card_bg = "#2C2C2C"
            self.text_color = "#FFFFFF"
            self.text_secondary = "#B4B4B4"
            self.accent_color = "#60CDFF"
            self.accent_hover = "#4FB8E6"
            self.border_color = "#3D3D3D"
        else:
            self.bg_color = "#F3F3F3"
            self.card_bg = "#FFFFFF"
            self.text_color = "#000000"
            self.text_secondary = "#605E5C"
            self.accent_color = "#0078D4"
            self.accent_hover = "#106EBE"
            self.border_color = "#E1DFDD"
        self.central = QWidget()
        self.central.setStyleSheet(f"background-color: {self.bg_color}; border-radius: 12px;")
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.title_bar = Title(self, self.bg_color, self.text_color)
        self.main_layout.addWidget(self.title_bar)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {self.bg_color};")
        self.main_layout.addWidget(self.stack)
        self.init_screen()
        self.progress_screen()
        self.stack.setCurrentWidget(self.init_widget)
        self.setWindowOpacity(0.0)
        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(300)
        self.fade.setStartValue(0.0)
        self.fade.setEndValue(1.0)
        self.fade.setEasingCurve(QEasingCurve.OutCubic)
        self.fade.start()
        self.show()

    def init_screen(self):
        self.init_widget = QWidget()
        self.init_widget.setStyleSheet(f"background-color: {self.bg_color};")
        layout = QVBoxLayout(self.init_widget)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(0)
        header = QLabel("OptiX")
        header.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {self.text_color}; padding: 0; margin: 0;")
        layout.addWidget(header)
        subtitle = QLabel("Windows Optimizer")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet(f"color: {self.text_secondary}; padding: 0; margin-top: 4px;")
        layout.addWidget(subtitle)
        layout.addSpacing(32)
        card = QWidget()
        card.setStyleSheet(f"""
            background-color: {self.card_bg};
            border: 0px solid {self.border_color};
            border-radius: 8px;
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)
        card_title = QLabel("Ready to optimize")
        card_title.setFont(QFont("Segoe UI", 14, QFont.Weight.DemiBold))
        card_title.setStyleSheet(f"color: {self.text_color};")
        card_layout.addWidget(card_title)
        card_desc = QLabel("Click the button below to start optimization process.\nThis process might take some time, depending on your Wi-Fi and PC components.")
        card_desc.setFont(QFont("Segoe UI", 9))
        card_desc.setStyleSheet(f"color: {self.text_secondary}; line-height: 1.5;")
        card_desc.setWordWrap(True)
        card_layout.addWidget(card_desc)
        card_layout.addSpacing(8)
        self.optimize_btn = QPushButton("Optimize now")
        self.optimize_btn.setFont(QFont("Segoe UI", 10))
        self.optimize_btn.setFixedHeight(36)
        self.optimize_btn.setCursor(Qt.PointingHandCursor)
        self.optimize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                background-color: {self.accent_hover};
            }}
            QPushButton:pressed {{
                background-color: {self.accent_color};
            }}
        """)
        self.optimize_btn.clicked.connect(self.start_optimization)
        card_layout.addWidget(self.optimize_btn)
        layout.addWidget(card)
        layout.addStretch()
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(16)
        footer_layout.addStretch()
        layout.addLayout(footer_layout)
        self.stack.addWidget(self.init_widget)

    def progress_screen(self):
        self.progress_widget = QWidget()
        self.progress_widget.setStyleSheet(f"background-color: {self.bg_color};")
        layout = QVBoxLayout(self.progress_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)
        progress_container = QWidget()
        progress_container.setStyleSheet(f"""
            background-color: {self.card_bg};
            border: 0px solid {self.border_color};
            border-radius: 8px;
        """)
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(32, 32, 32, 32)
        progress_layout.setSpacing(20)
        self.progress_title = QLabel("")
        self.progress_title.setFont(QFont("Segoe UI", 18, QFont.Weight.DemiBold))
        self.progress_title.setStyleSheet(f"color: {self.text_color};")
        self.progress_title.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.progress_title)
        self.progress_label = QLabel("Preparing...")
        self.progress_label.setFont(QFont("Segoe UI", 10))
        self.progress_label.setStyleSheet(f"text-align: left; color: {self.text_secondary};")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setMinimumHeight(20)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addSpacing(8)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {self.border_color};
            }}
            QProgressBar::chunk {{
                background-color: {self.accent_color};
                border-radius: 4px;
                width: 1px;
            }}
        """)
        progress_layout.addWidget(self.progress_bar)
        self.percent_label = QLabel("0%")
        self.percent_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        self.percent_label.setStyleSheet(f"color: {self.text_color};")
        self.percent_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.percent_label)
        layout.addWidget(progress_container)
        self.stack.addWidget(self.progress_widget)

    def start_optimization(self):
        self.optimize_btn.setEnabled(False)
        self.stack.setCurrentWidget(self.progress_widget)
        QTimer.singleShot(100, self.run_worker)

    def run_worker(self):
        self.worker = Worker()
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.start()

    def update_progress(self, current, total, task_name=""):
        percent = int((current / total) * 100)
        
        self.progress_bar.setValue(percent)


        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {self.border_color};
            }}
            QProgressBar::chunk {{
                background-color: {self.accent_color};
                border-radius: 4px;
            }}
        """)

        self.progress_title.setText("Sit tight and relax.")
        self.progress_label.setText(task_name)
        self.percent_label.setText(f"{percent}%")

        if current == total:
            QTimer.singleShot(300, self.show_completion)

    def show_completion(self):
        self.progress_title.setText("Complete")
        self.progress_title.setStyleSheet(f"color: #10B981;")
        self.progress_label.setText("Your system has been optimized successfully.")
        os.system("shutdown -r -t 5 -f -c 'System needs to reboot in order to apply OptiX optimizations'")
