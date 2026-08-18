import sys
import os
import platform
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame,
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QCursor, QColor

# Professional Light Theme QSS
LIGHT_THEME = """
    QWidget {
        background-color: #F9FAFB;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    QLabel {
        background: transparent;
        color: #111827;
    }
    QLabel#headerTitle {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    QLabel#subtitleLabel {
        font-size: 14px;
        color: #6B7280;
    }
    QLabel#fieldLabel {
        font-size: 12px;
        font-weight: 700;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    QLabel#statusLabel {
        font-size: 13px;
        color: #6B7280;
        font-weight: 500;
        margin-top: 8px;
    }
    QFrame#mainCard {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }
    QLineEdit {
        background-color: #F3F4F6;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        padding: 0px 15px;
        min-height: 45px;
        color: #111827;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #2563EB;
        background-color: #FFFFFF;
        padding: 0px 14px;
    }
    QPushButton {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    QPushButton#primaryBtn {
        background-color: #2563EB;
        color: #FFFFFF;
        border-radius: 6px;
        padding: 0px 20px;
        min-height: 45px;
        font-size: 15px;
        font-weight: 600;
        border: none;
    }
    QPushButton#primaryBtn:hover {
        background-color: #1D4ED8;
    }
    QPushButton#primaryBtn:disabled {
        background-color: #9CA3AF;
        color: #F3F4F6;
    }
    QPushButton#secondaryBtn {
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        padding: 0px 20px;
        min-height: 45px;
        font-size: 13px;
        font-weight: 600;
    }
    QPushButton#secondaryBtn:hover {
        background-color: #F3F4F6;
        color: #111827;
    }
    QPushButton#themeBtn {
        background-color: transparent;
        color: #4B5563;
        font-size: 13px;
        font-weight: 600;
        border-radius: 6px;
        border: 1px solid #D1D5DB;
        padding: 6px 12px;
        min-height: 30px;
    }
    QPushButton#themeBtn:hover {
        background-color: #E5E7EB;
        color: #111827;
    }
"""

# Professional Dark Theme QSS
DARK_THEME = """
    QWidget {
        background-color: #111827;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    QLabel {
        background: transparent;
        color: #F9FAFB;
    }
    QLabel#headerTitle {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    QLabel#subtitleLabel {
        font-size: 14px;
        color: #9CA3AF;
    }
    QLabel#fieldLabel {
        font-size: 12px;
        font-weight: 700;
        color: #D1D5DB;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    QLabel#statusLabel {
        font-size: 13px;
        color: #9CA3AF;
        font-weight: 500;
        margin-top: 8px;
    }
    QFrame#mainCard {
        background-color: #1F2937;
        border-radius: 12px;
        border: 1px solid #374151;
    }
    QLineEdit {
        background-color: #111827;
        border: 1px solid #4B5563;
        border-radius: 6px;
        padding: 0px 15px;
        min-height: 45px;
        color: #F9FAFB;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #3B82F6;
        padding: 0px 14px;
    }
    QPushButton {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    QPushButton#primaryBtn {
        background-color: #2563EB;
        color: #FFFFFF;
        border-radius: 6px;
        padding: 0px 20px;
        min-height: 45px;
        font-size: 15px;
        font-weight: 600;
        border: none;
    }
    QPushButton#primaryBtn:hover {
        background-color: #3B82F6;
    }
    QPushButton#primaryBtn:disabled {
        background-color: #4B5563;
        color: #9CA3AF;
    }
    QPushButton#secondaryBtn {
        background-color: #374151;
        color: #F9FAFB;
        border: 1px solid #4B5563;
        border-radius: 6px;
        padding: 0px 20px;
        min-height: 45px;
        font-size: 13px;
        font-weight: 600;
    }
    QPushButton#secondaryBtn:hover {
        background-color: #4B5563;
        border-color: #6B7280;
    }
    QPushButton#themeBtn {
        background-color: transparent;
        color: #D1D5DB;
        font-size: 13px;
        font-weight: 600;
        border-radius: 6px;
        border: 1px solid #4B5563;
        padding: 6px 12px;
        min-height: 30px;
    }
    QPushButton#themeBtn:hover {
        background-color: #374151;
        color: #FFFFFF;
    }
"""

class OpenModelicaRunnerApp(QWidget):
    """
    A PyQt6 Desktop Application to run OpenModelica executables.
    Features dark/light mode, robust error handling, and PEP8 compliance.
    """

    def __init__(self) -> None:
        """Initialize the application state and UI components."""
        super().__init__()
        self.is_dark_mode = True
        self.process = None
        self.init_ui()

    def init_ui(self) -> None:
        """Construct the UI layout and widgets."""
        self.setWindowTitle("OpenModelica Simulation Runner")
        self.setMinimumSize(800, 600)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Top Bar (Header) ---
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(40, 30, 40, 20)
        
        titles_layout = QVBoxLayout()
        titles_layout.setSpacing(4)
        title = QLabel("OpenModelica Runner")
        title.setObjectName("headerTitle")
        subtitle = QLabel("Configure and execute your compiled simulation models")
        subtitle.setObjectName("subtitleLabel")
        titles_layout.addWidget(title)
        titles_layout.addWidget(subtitle)
        
        self.theme_btn = QPushButton("Toggle Light Mode")
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        top_bar_layout.addLayout(titles_layout)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.theme_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        main_layout.addWidget(top_bar)

        # --- Content Area ---
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 10, 40, 40)
        
        # Card Container
        card = QFrame()
        card.setObjectName("mainCard")
        
        # Drop Shadow for Card
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setOffset(0, 4)
        card.setGraphicsEffect(self.shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(25)

        # 1. Executable Input Group
        exe_group = QVBoxLayout()
        exe_group.setSpacing(8)
        exe_label = QLabel("Executable Path")
        exe_label.setObjectName("fieldLabel")
        
        exe_input_layout = QHBoxLayout()
        exe_input_layout.setSpacing(12)
        self.exe_path_input = QLineEdit()
        self.exe_path_input.setPlaceholderText("Select your OpenModelica binary file...")
        self.exe_path_input.textChanged.connect(self.check_ready_state)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        browse_btn.clicked.connect(self.browse_executable)
        
        exe_input_layout.addWidget(self.exe_path_input)
        exe_input_layout.addWidget(browse_btn)
        
        exe_group.addWidget(exe_label)
        exe_group.addLayout(exe_input_layout)
        card_layout.addLayout(exe_group)

        # 2. Time Inputs Group
        time_layout = QHBoxLayout()
        time_layout.setSpacing(25)

        start_col = QVBoxLayout()
        start_col.setSpacing(8)
        start_label = QLabel("Start Time")
        start_label.setObjectName("fieldLabel")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("e.g., 0")
        self.start_time_input.textChanged.connect(self.check_ready_state)
        start_col.addWidget(start_label)
        start_col.addWidget(self.start_time_input)
        
        stop_col = QVBoxLayout()
        stop_col.setSpacing(8)
        stop_label = QLabel("Stop Time")
        stop_label.setObjectName("fieldLabel")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("e.g., 4")
        self.stop_time_input.textChanged.connect(self.check_ready_state)
        stop_col.addWidget(stop_label)
        stop_col.addWidget(self.stop_time_input)

        time_layout.addLayout(start_col)
        time_layout.addLayout(stop_col)
        card_layout.addLayout(time_layout)

        # Spacer before button
        card_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # 3. Action Button
        self.run_btn = QPushButton("Initialize Simulation")
        self.run_btn.setObjectName("primaryBtn")
        self.run_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self.validate_and_run)
        card_layout.addWidget(self.run_btn)
        
        # 4. Status Label
        self.status_label = QLabel("Awaiting input parameters...")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.status_label)

        content_layout.addWidget(card)
        content_layout.addStretch()
        main_layout.addWidget(content_area)

        # Apply initial theme
        self.apply_theme()

    def toggle_theme(self) -> None:
        """Switch between dark and light themes."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self) -> None:
        """Apply the CSS stylesheet corresponding to the current theme state."""
        if self.is_dark_mode:
            self.setStyleSheet(DARK_THEME)
            self.theme_btn.setText("Switch to Light Mode")
            self.shadow.setColor(QColor(0, 0, 0, 40))
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.theme_btn.setText("Switch to Dark Mode")
            self.shadow.setColor(QColor(0, 0, 0, 15))
            
        self.update_status_color()

    def update_status_color(self) -> None:
        """Update the status label color based on its text and current theme."""
        text = self.status_label.text()
        if "completed successfully" in text:
            color = "#10B981" # Emerald
        elif "failed" in text or "Error" in text:
            color = "#EF4444" # Red
        elif "Running" in text:
            color = "#3B82F6" # Blue
        else:
            color = "#9CA3AF" if self.is_dark_mode else "#6B7280" # Gray
            
        self.status_label.setStyleSheet(f"color: {color};")

    def check_ready_state(self) -> None:
        """Enable the run button only if all required inputs are populated."""
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
        self.update_status_color()

    def browse_executable(self) -> None:
        """Open a file dialog to select the OpenModelica binary."""
        file_filter = "All Files (*);;Executable Files (*.exe)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select OpenModelica Executable", "", file_filter
        )
        if file_path:
            self.exe_path_input.setText(file_path)

    def validate_and_run(self) -> None:
        """Validate inputs based on FOSSEE criteria and trigger execution."""
        exe_path = self.exe_path_input.text().strip()
        start_str = self.start_time_input.text().strip()
        stop_str = self.stop_time_input.text().strip()

        if not os.path.isfile(exe_path):
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

        self.run_executable(exe_path, start_time, stop_time)

    def run_executable(self, exe_path: str, start_time: int, stop_time: int) -> None:
        """
        Execute the compiled binary with QProcess to prevent UI blocking.
        Automatically detects the OS and runs accordingly:
        - Linux/macOS: Executes the binary directly via shell.
        - Windows: Routes the binary through WSL for Unix compatibility.
        
        Args:
            exe_path (str): Absolute path to the OpenModelica binary.
            start_time (int): Simulation start time.
            stop_time (int): Simulation stop time.
        """
        # Using the hint specified -override flag
        sim_args = ["-override", f"startTime={start_time},stopTime={stop_time}"]

        current_os = platform.system()

        if current_os == "Windows":
            # Windows: Run the Linux ELF binary through WSL
            program = "wsl"
            args = [exe_path] + sim_args
        else:
            # Linux / macOS: Run the binary directly
            # Ensure the binary has execute permissions
            if not os.access(exe_path, os.X_OK):
                os.chmod(exe_path, 0o755)
            program = exe_path
            args = sim_args

        self.run_btn.setEnabled(False)
        self.run_btn.setText("Executing Sequence...")
        self.status_label.setText(f"Running on {current_os}...")
        self.update_status_color()

        self.process = QProcess(self)
        self.process.finished.connect(self.on_process_finished)
        self.process.errorOccurred.connect(self.on_process_error)
        self.process.start(program, args)

    def on_process_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        """Handle process completion, capturing stdout/stderr."""
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Initialize Simulation")

        if exit_code == 0 and exit_status == QProcess.ExitStatus.NormalExit:
            self.status_label.setText("Simulation completed successfully.")
            self.update_status_color()
            
            stdout = self.process.readAllStandardOutput().data().decode().strip()
            msg = "Simulation finished successfully."
            if stdout:
                msg += f"\n\n--- Executable Output ---\n{stdout}"
            
            self.show_success_message("Success", msg)
        else:
            self.status_label.setText(f"Process failed (Exit: {exit_code}).")
            self.update_status_color()
            
            stderr = self.process.readAllStandardError().data().decode().strip()
            stdout = self.process.readAllStandardOutput().data().decode().strip()
            
            err_msg = "Process failed."
            if stderr:
                err_msg += f"\n\n[STDERR]\n{stderr}"
            if stdout:
                err_msg += f"\n\n[STDOUT]\n{stdout}"
                
            self.show_error_message("Execution Error", err_msg)

    def on_process_error(self, error: QProcess.ProcessError) -> None:
        """Handle failure to launch the executable."""
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Initialize Simulation")
        self.status_label.setText("Launch failed.")
        self.update_status_color()
        
        self.show_error_message("Process Error", f"Failed to start: {self.process.errorString()}")

    def show_error_message(self, title: str, message: str) -> None:
        """Display a styled critical error dialog."""
        msg_box = QMessageBox(self)
        self._style_msg_box(msg_box)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
        
    def show_success_message(self, title: str, message: str) -> None:
        """Display a styled information dialog."""
        msg_box = QMessageBox(self)
        self._style_msg_box(msg_box)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
        
    def _style_msg_box(self, msg_box: QMessageBox) -> None:
        """Helper to style message boxes according to current theme."""
        if self.is_dark_mode:
            msg_box.setStyleSheet("QMessageBox { background-color: #1F2937; } QLabel { color: #F9FAFB; } QPushButton { background-color: #2563EB; color: white; border-radius: 4px; padding: 6px 16px; }")
        else:
            msg_box.setStyleSheet("QMessageBox { background-color: #FFFFFF; } QLabel { color: #111827; } QPushButton { background-color: #2563EB; color: white; border-radius: 4px; padding: 6px 16px; }")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = OpenModelicaRunnerApp()
    window.show()
    sys.exit(app.exec())
