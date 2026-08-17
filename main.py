import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt, QProcess


class OpenModelicaRunnerApp(QWidget):
    """
    A PyQt6 GUI application to run an OpenModelica executable with specified start and stop times.
    """
    
    def __init__(self):
        super().__init__()
        self.process = None
        self.init_ui()

    def init_ui(self):
        """Initializes the User Interface layout and components."""
        self.setWindowTitle("OpenModelica Premium Runner")
        self.resize(600, 350)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header Title
        title_label = QLabel("OpenModelica Execution Setup")
        title_label.setObjectName("headerTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Group box for configuration
        config_group = QGroupBox("Simulation Parameters")
        config_layout = QVBoxLayout()
        config_layout.setContentsMargins(20, 30, 20, 20)
        config_layout.setSpacing(15)

        # 1. Executable Path Selection
        exe_layout = QHBoxLayout()
        self.exe_path_label = QLabel("Executable Path:")
        self.exe_path_input = QLineEdit()
        self.exe_path_input.setPlaceholderText("Select the OpenModelica executable (.exe)...")
        self.exe_browse_btn = QPushButton("Browse")
        self.exe_browse_btn.setObjectName("browseBtn")
        self.exe_browse_btn.clicked.connect(self.browse_executable)
        
        exe_layout.addWidget(self.exe_path_label)
        exe_layout.addWidget(self.exe_path_input)
        exe_layout.addWidget(self.exe_browse_btn)

        # 2. Start Time Input
        start_layout = QHBoxLayout()
        self.start_time_label = QLabel("Start Time (Int):")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("e.g., 0")
        
        start_layout.addWidget(self.start_time_label)
        start_layout.addWidget(self.start_time_input)

        # 3. Stop Time Input
        stop_layout = QHBoxLayout()
        self.stop_time_label = QLabel("Stop Time (Int):")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("e.g., 4")
        
        stop_layout.addWidget(self.stop_time_label)
        stop_layout.addWidget(self.stop_time_input)

        # Add sub-layouts to config group
        config_layout.addLayout(exe_layout)
        config_layout.addLayout(start_layout)
        config_layout.addLayout(stop_layout)
        config_group.setLayout(config_layout)

        # 4. Run Button
        self.run_btn = QPushButton("🚀 Run Simulation")
        self.run_btn.setObjectName("runBtn")
        self.run_btn.setMinimumHeight(45)
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_executable)

        # Output / Status label
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add everything to main layout
        main_layout.addWidget(config_group)
        main_layout.addStretch()
        main_layout.addWidget(self.run_btn)
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)

    def browse_executable(self):
        """Opens a file dialog to select the executable file."""
        file_filter = "Executable Files (*.exe);;All Files (*)" if os.name == 'nt' else "All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select OpenModelica Executable", "", file_filter
        )
        if file_path:
            self.exe_path_input.setText(file_path)

    def validate_inputs(self):
        """
        Validates the inputs based on the condition:
        0 <= start time < stop time < 5
        """
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

        # Test Condition: 0 <= start time < stop time < 5
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
        """Executes the selected program with start and stop time arguments using QProcess."""
        if not self.validate_inputs():
            return

        exe_path = self.exe_path_input.text().strip()
        start_time = self.start_time_input.text().strip()
        stop_time = self.stop_time_input.text().strip()

        args = ["-override", f"startTime={start_time},stopTime={stop_time}"]

        # Disable button while running
        self.run_btn.setEnabled(False)
        self.run_btn.setText("⏳ Running...")
        self.status_label.setText("Executing simulation in background...")
        self.status_label.setStyleSheet("color: #60a5fa;") # Tailwind blue-400

        # Set up QProcess
        self.process = QProcess(self)
        self.process.finished.connect(self.on_process_finished)
        self.process.errorOccurred.connect(self.on_process_error)
        
        self.process.start(exe_path, args)

    def on_process_finished(self, exit_code, exit_status):
        """Callback when the executable finishes."""
        self.run_btn.setEnabled(True)
        self.run_btn.setText("🚀 Run Simulation")
        
        if exit_code == 0:
            self.status_label.setText("Simulation completed successfully.")
            self.status_label.setStyleSheet("color: #34d399;") # Tailwind emerald-400
            QMessageBox.information(self, "Success", "The OpenModelica simulation completed successfully.")
        else:
            self.status_label.setText(f"Simulation failed with exit code {exit_code}.")
            self.status_label.setStyleSheet("color: #f87171;") # Tailwind red-400
            
            stderr = self.process.readAllStandardError().data().decode().strip()
            error_msg = f"Process exited with code {exit_code}."
            if stderr:
                error_msg += f"\n\nError output:\n{stderr}"
            self.show_error_message("Execution Error", error_msg)

    def on_process_error(self, error):
        """Callback for process-level errors (e.g., file not executable)."""
        self.run_btn.setEnabled(True)
        self.run_btn.setText("🚀 Run Simulation")
        self.status_label.setText("Error launching process.")
        self.status_label.setStyleSheet("color: #f87171;")
        self.show_error_message("Process Error", f"Failed to start the process: {self.process.errorString()}")

    def show_error_message(self, title, message):
        """Helper to show error popups."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


def apply_premium_stylesheet(app):
    """Applies a modern, premium dark theme to the PyQt6 application via QSS."""
    qss = """
    /* Main Window Background */
    QWidget {
        background-color: #0f172a; /* Tailwind slate-900 */
        color: #f8fafc; /* Tailwind slate-50 */
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 14px;
    }

    /* Labels */
    QLabel {
        color: #cbd5e1; /* Tailwind slate-300 */
    }
    
    QLabel#headerTitle {
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
    }

    QLabel#statusLabel {
        font-size: 13px;
        color: #94a3b8; /* Tailwind slate-400 */
        margin-top: 10px;
    }

    /* Input Fields */
    QLineEdit {
        background-color: #1e293b; /* Tailwind slate-800 */
        border: 1px solid #334155; /* Tailwind slate-700 */
        border-radius: 6px;
        padding: 8px 12px;
        color: #f8fafc;
        selection-background-color: #4f46e5;
    }
    
    QLineEdit:focus {
        border: 1px solid #6366f1; /* Tailwind indigo-500 */
        background-color: #0f172a;
    }

    /* Buttons */
    QPushButton {
        background-color: #334155; /* Tailwind slate-700 */
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        color: #f8fafc;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: #475569; /* Tailwind slate-600 */
    }

    QPushButton:pressed {
        background-color: #1e293b; /* Tailwind slate-800 */
    }

    /* Primary Run Button */
    QPushButton#runBtn {
        background-color: #4f46e5; /* Tailwind indigo-600 */
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
    }

    QPushButton#runBtn:hover {
        background-color: #6366f1; /* Tailwind indigo-500 */
    }
    
    QPushButton#runBtn:pressed {
        background-color: #4338ca; /* Tailwind indigo-700 */
    }
    
    QPushButton#runBtn:disabled {
        background-color: #334155;
        color: #94a3b8;
    }

    /* Browse Button */
    QPushButton#browseBtn {
        background-color: #0ea5e9; /* Tailwind sky-500 */
    }
    QPushButton#browseBtn:hover {
        background-color: #38bdf8; /* Tailwind sky-400 */
    }

    /* Group Box */
    QGroupBox {
        border: 1px solid #334155;
        border-radius: 8px;
        margin-top: 1.5em;
        padding-top: 10px;
        background-color: #0b1120;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 15px;
        padding: 0 5px;
        color: #38bdf8; /* Tailwind sky-400 */
        font-weight: bold;
    }
    
    /* Dialogs (Message Boxes) */
    QMessageBox {
        background-color: #0f172a;
    }
    QMessageBox QLabel {
        color: #f8fafc;
    }
    QMessageBox QPushButton {
        min-width: 80px;
        background-color: #4f46e5;
    }
    """
    app.setStyleSheet(qss)


def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    
    # Apply standard modern style base, then apply our premium QSS on top
    app.setStyle('Fusion')
    apply_premium_stylesheet(app)
    
    runner = OpenModelicaRunnerApp()
    runner.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
