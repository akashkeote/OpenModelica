import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QCursor, QColor

LIGHT_THEME = """
    QWidget {
        background-color: #fafaf9;
        color: #1c1917;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    QLabel#headerTitle {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: 1px;
    }
    QLabel#subtitleLabel {
        font-size: 13px;
        color: #64748b;
    }
    QLabel#fieldLabel {
        font-size: 12px;
        font-weight: 700;
        color: #475569;
        letter-spacing: 1px;
    }
    QFrame#mainCard {
        background-color: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
    }
    QLineEdit {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 12px;
        color: #0f172a;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #3b82f6;
        background-color: #ffffff;
    }
    QPushButton#primaryBtn {
        background-color: #0f172a;
        color: white;
        border-radius: 10px;
        padding: 14px;
        font-size: 15px;
        font-weight: bold;
    }
    QPushButton#primaryBtn:hover {
        background-color: #1e293b;
    }
    QPushButton#primaryBtn:disabled {
        background-color: #94a3b8;
    }
    QPushButton#secondaryBtn {
        background-color: #f1f5f9;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    QPushButton#secondaryBtn:hover {
        background-color: #e2e8f0;
    }
    QPushButton#themeBtn {
        background-color: transparent;
        color: #0f172a;
        font-size: 13px;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 6px 12px;
    }
    QPushButton#themeBtn:hover {
        background-color: #e2e8f0;
    }
"""

DARK_THEME = """
    QWidget {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    QLabel#headerTitle {
        font-size: 26px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: 1px;
    }
    QLabel#subtitleLabel {
        font-size: 13px;
        color: #94a3b8;
    }
    QLabel#fieldLabel {
        font-size: 12px;
        font-weight: 700;
        color: #cbd5e1;
        letter-spacing: 1px;
    }
    QFrame#mainCard {
        background-color: #1e293b;
        border-radius: 16px;
        border: 1px solid #334155;
    }
    QLineEdit {
        background-color: #0f172a;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 12px;
        color: #f8fafc;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #3b82f6;
    }
    QPushButton#primaryBtn {
        background-color: #3b82f6;
        color: white;
        border-radius: 10px;
        padding: 14px;
        font-size: 15px;
        font-weight: bold;
    }
    QPushButton#primaryBtn:hover {
        background-color: #2563eb;
    }
    QPushButton#primaryBtn:disabled {
        background-color: #475569;
        color: #94a3b8;
    }
    QPushButton#secondaryBtn {
        background-color: #334155;
        color: #f8fafc;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    QPushButton#secondaryBtn:hover {
        background-color: #475569;
    }
    QPushButton#themeBtn {
        background-color: transparent;
        color: #f8fafc;
        font-size: 13px;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #475569;
        padding: 6px 12px;
    }
    QPushButton#themeBtn:hover {
        background-color: #334155;
    }
"""

class OpenModelicaRunnerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("OpenModelica Simulation Runner")
        self.setMinimumSize(750, 550)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 40)
        main_layout.setSpacing(30)
        
        # --- Header with Theme Toggle ---
        header_layout = QHBoxLayout()
        
        titles_layout = QVBoxLayout()
        title = QLabel("OPENMODELICA SIMULATION")
        title.setObjectName("headerTitle")
        subtitle = QLabel("Configure your OpenModelica executable parameters below.")
        subtitle.setObjectName("subtitleLabel")
        titles_layout.addWidget(title)
        titles_layout.addWidget(subtitle)
        
        self.theme_btn = QPushButton("Dark Mode")
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        header_layout.addLayout(titles_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)

        # --- Main Card ---
        card = QFrame()
        card.setObjectName("mainCard")
        
        # Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor(0, 0, 0, 15))
        self.shadow.setOffset(0, 10)
        card.setGraphicsEffect(self.shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(25)

        # 1. Executable Input
        exe_label = QLabel("EXECUTABLE PATH")
        exe_label.setObjectName("fieldLabel")
        card_layout.addWidget(exe_label)
        
        exe_layout = QHBoxLayout()
        exe_layout.setSpacing(15)
        self.exe_path_input = QLineEdit()
        self.exe_path_input.setPlaceholderText("Select the compiled OpenModelica binary...")
        self.exe_path_input.textChanged.connect(self.check_ready_state)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        browse_btn.clicked.connect(self.browse_executable)
        
        exe_layout.addWidget(self.exe_path_input)
        exe_layout.addWidget(browse_btn)
        card_layout.addLayout(exe_layout)

        # 2. Time Inputs
        time_layout = QHBoxLayout()
        time_layout.setSpacing(20)

        start_col = QVBoxLayout()
        start_label = QLabel("START TIME")
        start_label.setObjectName("fieldLabel")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("e.g. 0")
        self.start_time_input.textChanged.connect(self.check_ready_state)
        start_col.addWidget(start_label)
        start_col.addWidget(self.start_time_input)
        
        stop_col = QVBoxLayout()
        stop_label = QLabel("STOP TIME")
        stop_label.setObjectName("fieldLabel")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("e.g. 4")
        self.stop_time_input.textChanged.connect(self.check_ready_state)
        stop_col.addWidget(stop_label)
        stop_col.addWidget(self.stop_time_input)

        time_layout.addLayout(start_col)
        time_layout.addLayout(stop_col)
        card_layout.addLayout(time_layout)

        # 3. Action Button
        self.run_btn = QPushButton("Initialize Simulation")
        self.run_btn.setObjectName("primaryBtn")
        self.run_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self.validate_and_run)
        card_layout.addWidget(self.run_btn)
        
        # 4. Status Label
        self.status_label = QLabel("Awaiting input parameters...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.status_label)

        main_layout.addWidget(card)
        main_layout.addStretch()

        self.apply_theme()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(DARK_THEME)
            self.theme_btn.setText("Light Mode")
            self.shadow.setColor(QColor(0, 0, 0, 50))
            # Fix dynamic status colors for dark mode
            if "completed successfully" in self.status_label.text():
                self.status_label.setStyleSheet("color: #10b981;") # emerald-500
            elif "failed" in self.status_label.text():
                self.status_label.setStyleSheet("color: #ef4444;") # red-500
            elif "Running" in self.status_label.text():
                self.status_label.setStyleSheet("color: #3b82f6;") # blue-500
            else:
                self.status_label.setStyleSheet("color: #94a3b8;") # slate-400
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.theme_btn.setText("Dark Mode")
            self.shadow.setColor(QColor(0, 0, 0, 15))
            # Fix dynamic status colors for light mode
            if "completed successfully" in self.status_label.text():
                self.status_label.setStyleSheet("color: #10b981;")
            elif "failed" in self.status_label.text():
                self.status_label.setStyleSheet("color: #ef4444;")
            elif "Running" in self.status_label.text():
                self.status_label.setStyleSheet("color: #3b82f6;")
            else:
                self.status_label.setStyleSheet("color: #64748b;") # slate-500

    def check_ready_state(self):
        is_ready = bool(
            self.exe_path_input.text().strip() and 
            self.start_time_input.text().strip() and 
            self.stop_time_input.text().strip()
        )
        self.run_btn.setEnabled(is_ready)
        if is_ready:
            self.status_label.setText("Ready to launch.")
        else:
            self.status_label.setText("Awaiting input parameters...")
        self.apply_theme() # refresh label color

    def browse_executable(self):
        file_filter = "All Files (*);;Executable Files (*.exe)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select OpenModelica Executable", "", file_filter
        )
        if file_path:
            self.exe_path_input.setText(file_path)

    def validate_and_run(self):
        start_str = self.start_time_input.text().strip()
        stop_str = self.stop_time_input.text().strip()
        exe_path = self.exe_path_input.text().strip()

        if not os.path.exists(exe_path):
            self.show_error_message("File Error", "The selected executable file does not exist.")
            return

        try:
            start_time = int(start_str)
            stop_time = int(stop_str)
        except ValueError:
            self.show_error_message("Validation Error", "Start time and Stop time must be valid integers.")
            return

        if not (0 <= start_time < stop_time < 5):
            self.show_error_message("Validation Error", "Please ensure the test condition is met:\n0 <= start time < stop time < 5")
            return

        # Hint specified -override
        args = ["-override", f"startTime={start_time},stopTime={stop_time}"]

        self.run_btn.setEnabled(False)
        self.run_btn.setText("Executing Sequence...")
        self.status_label.setText("Running OpenModelica simulation...")
        self.apply_theme() # Refresh dynamic color

        self.process = QProcess(self)
        self.process.finished.connect(self.on_process_finished)
        self.process.errorOccurred.connect(self.on_process_error)
        self.process.start(exe_path, args)

    def on_process_finished(self, exit_code, exit_status):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Initialize Simulation")

        if exit_code == 0 and exit_status == QProcess.ExitStatus.NormalExit:
            self.status_label.setText("Simulation completed successfully.")
            self.apply_theme()
            
            stdout = self.process.readAllStandardOutput().data().decode().strip()
            msg = "Simulation finished successfully."
            if stdout:
                msg += f"\n\n--- Executable Output ---\n{stdout}"
            QMessageBox.information(self, "Success", msg)
        else:
            self.status_label.setText(f"Process failed (Exit: {exit_code}).")
            self.apply_theme()
            
            stderr = self.process.readAllStandardError().data().decode().strip()
            stdout = self.process.readAllStandardOutput().data().decode().strip()
            
            err_msg = "Process failed."
            if stderr:
                err_msg += f"\n\n[STDERR]\n{stderr}"
            if stdout:
                err_msg += f"\n\n[STDOUT]\n{stdout}"
                
            self.show_error_message("Execution Error", err_msg)

    def on_process_error(self, error):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Initialize Simulation")
        self.status_label.setText("Launch failed.")
        self.apply_theme()
        self.show_error_message("Process Error", f"Failed to start: {self.process.errorString()}")

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        if self.is_dark_mode:
            msg_box.setStyleSheet("background-color: #1e293b; color: #f8fafc;")
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = OpenModelicaRunnerApp()
    window.show()
    sys.exit(app.exec())
