import sys
import os
import urllib.request
import ssl
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QGroupBox, QGraphicsDropShadowEffect, QFrame
)
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QFontDatabase, QColor, QFont

def load_custom_fonts():
    """Downloads and loads custom fonts from CDNs."""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except Exception:
        pass

    fonts = {
        "SpaceGrotesk-Regular.ttf": "https://cdn.jsdelivr.net/gh/floriankarsten/space-grotesk@master/fonts/ttf/static/SpaceGrotesk-Regular.ttf",
        "DotGothic16-Regular.ttf": "https://cdn.jsdelivr.net/gh/fontworks-fonts/DotGothic16@master/fonts/ttf/DotGothic16-Regular.ttf"
    }
    
    font_families = []
    for filename, url in fonts.items():
        if not os.path.exists(filename):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Download failed for {filename}: {e}")
        
        if os.path.exists(filename):
            font_id = QFontDatabase.addApplicationFont(filename)
            if font_id != -1:
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                font_families.append(family)
    return font_families


class OpenModelicaRunnerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.process = None
        self.init_ui()

    def add_shadow(self, widget, blur_radius=15, alpha=30, offset=(0, 4)):
        """Utility to add soft UI/UX shadows to widgets."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur_radius)
        shadow.setColor(QColor(0, 0, 0, alpha))
        shadow.setOffset(offset[0], offset[1])
        widget.setGraphicsEffect(shadow)

    def init_ui(self):
        self.setWindowTitle("OpenModelica Arcade Runner")
        self.resize(650, 420)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Main Layout Container
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Header Title
        self.title_label = QLabel("ARCADE.26 SIMULATION")
        self.title_label.setObjectName("headerTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel("Configure your OpenModelica executable parameters below.")
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.subtitle_label)

        # Main Card (Container)
        card = QFrame()
        card.setObjectName("mainCard")
        self.add_shadow(card, blur_radius=25, alpha=15, offset=(0, 8))
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)

        # 1. Executable Path
        exe_layout = QHBoxLayout()
        self.exe_path_input = QLineEdit()
        self.exe_path_input.setPlaceholderText("Path to .exe file...")
        self.exe_browse_btn = QPushButton("Browse")
        self.exe_browse_btn.setObjectName("browseBtn")
        self.exe_browse_btn.clicked.connect(self.browse_executable)
        
        exe_layout.addWidget(self.exe_path_input)
        exe_layout.addWidget(self.exe_browse_btn)

        # 2. Start/Stop Time Row
        time_layout = QHBoxLayout()
        time_layout.setSpacing(15)

        # Start Time
        start_col = QVBoxLayout()
        self.start_time_label = QLabel("START TIME")
        self.start_time_label.setObjectName("fieldLabel")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("0")
        start_col.addWidget(self.start_time_label)
        start_col.addWidget(self.start_time_input)

        # Stop Time
        stop_col = QVBoxLayout()
        self.stop_time_label = QLabel("STOP TIME")
        self.stop_time_label.setObjectName("fieldLabel")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("4")
        stop_col.addWidget(self.stop_time_label)
        stop_col.addWidget(self.stop_time_input)

        time_layout.addLayout(start_col)
        time_layout.addLayout(stop_col)

        # Add to card
        card_layout.addWidget(QLabel("EXECUTABLE", objectName="fieldLabel"))
        card_layout.addLayout(exe_layout)
        card_layout.addLayout(time_layout)

        # Run Button
        self.run_btn = QPushButton("Initialize Simulation")
        self.run_btn.setObjectName("runBtn")
        self.run_btn.setMinimumHeight(48)
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_executable)
        self.add_shadow(self.run_btn, blur_radius=15, alpha=40, offset=(0, 4))
        card_layout.addWidget(self.run_btn)

        # Status Label inside card
        self.status_label = QLabel("Ready for execution.")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.status_label)

        main_layout.addWidget(card)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def browse_executable(self):
        file_filter = "Executable Files (*.exe);;All Files (*)" if os.name == 'nt' else "All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select OpenModelica Executable", "", file_filter
        )
        if file_path:
            self.exe_path_input.setText(file_path)

    def validate_inputs(self):
        exe_path = self.exe_path_input.text().strip()
        if not exe_path:
            self.show_error_message("Validation Error", "Please select an executable file.")
            return False

        if not os.path.isfile(exe_path):
            self.show_error_message("Validation Error", f"The file '{exe_path}' does not exist.")
            return False

        start_str = self.start_time_input.text().strip()
        stop_str = self.stop_time_input.text().strip()

        if not start_str or not stop_str:
            self.show_error_message("Validation Error", "Please enter both Start Time and Stop Time.")
            return False

        try:
            start_time = int(start_str)
            stop_time = int(stop_str)
        except ValueError:
            self.show_error_message("Validation Error", "Start Time and Stop Time must be integers.")
            return False

        if not (0 <= start_time):
            self.show_error_message("Validation Error", "Start time must be >= 0.")
            return False
        if not (start_time < stop_time):
            self.show_error_message("Validation Error", "Start time must be strictly less than Stop time.")
            return False
        if not (stop_time < 5):
            self.show_error_message("Validation Error", "Stop time must be strictly less than 5.")
            return False

        return True

    def run_executable(self):
        if not self.validate_inputs():
            return

        exe_path = self.exe_path_input.text().strip()
        start_time = self.start_time_input.text().strip()
        stop_time = self.stop_time_input.text().strip()
        args = ["-override", f"startTime={start_time},stopTime={stop_time}"]

        self.run_btn.setEnabled(False)
        self.run_btn.setText("Executing Sequence...")
        self.status_label.setText("Background process running...")
        self.status_label.setStyleSheet("color: #3b82f6;") # blue-500

        self.process = QProcess(self)
        self.process.finished.connect(self.on_process_finished)
        self.process.errorOccurred.connect(self.on_process_error)
        self.process.start(exe_path, args)

    def on_process_finished(self, exit_code, exit_status):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Initialize Simulation")
        
        if exit_code == 0:
            self.status_label.setText("Simulation completed successfully.")
            self.status_label.setStyleSheet("color: #10b981;") # emerald-500
            QMessageBox.information(self, "Success", "Simulation finished successfully.")
        else:
            self.status_label.setText(f"Process failed (Exit: {exit_code}).")
            self.status_label.setStyleSheet("color: #ef4444;") # red-500
            stderr = self.process.readAllStandardError().data().decode().strip()
            self.show_error_message("Execution Error", f"Process failed.\n{stderr}")

    def on_process_error(self, error):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Initialize Simulation")
        self.status_label.setText("Launch failed.")
        self.status_label.setStyleSheet("color: #ef4444;")
        self.show_error_message("Process Error", f"Failed to start: {self.process.errorString()}")

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


def apply_premium_stylesheet(app):
    """Ultimate UI/UX Designer Premium StyleSheet."""
    qss = """
    /* Main Background */
    QWidget {
        background-color: #fafaf9; /* Warm very light gray (stone-50) */
        color: #1c1917; /* Dark stone */
        font-family: 'Space Grotesk', 'Inter', 'Segoe UI', sans-serif;
        font-size: 14px;
    }

    /* Typography */
    QLabel#headerTitle {
        font-family: 'DotGothic16', 'Courier New', monospace;
        font-size: 26px;
        color: #0f172a; /* Slate 900 */
        letter-spacing: 2px;
        margin-bottom: 0px;
    }

    QLabel#subtitleLabel {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        color: #78716c; /* Stone 500 */
        margin-bottom: 10px;
    }

    QLabel#fieldLabel {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 11px;
        font-weight: bold;
        color: #57534e; /* Stone 600 */
        letter-spacing: 1px;
    }

    QLabel#statusLabel {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        color: #a8a29e; /* Stone 400 */
        margin-top: 5px;
    }

    /* Main Card */
    QFrame#mainCard {
        background-color: #ffffff;
        border-radius: 16px;
        border: 1px solid #e7e5e4; /* Stone 200 */
    }

    /* Inputs */
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #d6d3d1; /* Stone 300 */
        border-radius: 8px;
        padding: 10px 14px;
        color: #292524;
        font-size: 13px;
    }
    
    QLineEdit:focus {
        border: 2px solid #0ea5e9; /* Sky 500 */
        padding: 9px 13px; /* Compensate for border width */
    }

    /* Buttons */
    QPushButton#browseBtn {
        background-color: #f5f5f4; /* Stone 100 */
        border: 1px solid #d6d3d1;
        border-radius: 8px;
        padding: 8px 16px;
        color: #44403c;
        font-weight: 600;
        font-size: 12px;
    }
    QPushButton#browseBtn:hover {
        background-color: #e7e5e4;
    }

    QPushButton#runBtn {
        background-color: #0f172a; /* Slate 900 */
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        letter-spacing: 0.5px;
        margin-top: 10px;
    }
    QPushButton#runBtn:hover {
        background-color: #1e293b; /* Slate 800 */
    }
    QPushButton#runBtn:pressed {
        background-color: #000000;
    }
    QPushButton#runBtn:disabled {
        background-color: #d6d3d1;
        color: #a8a29e;
    }

    /* Message Boxes */
    QMessageBox {
        background-color: #ffffff;
    }
    QMessageBox QPushButton {
        background-color: #0f172a;
        color: #ffffff;
        border-radius: 6px;
        padding: 6px 20px;
        min-width: 80px;
    }
    """
    app.setStyleSheet(qss)


def main():
    app = QApplication(sys.argv)
    
    # Enable high DPI scaling for crisp UI
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Load fonts
    load_custom_fonts()
    
    app.setStyle('Fusion')
    apply_premium_stylesheet(app)
    
    runner = OpenModelicaRunnerApp()
    runner.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
