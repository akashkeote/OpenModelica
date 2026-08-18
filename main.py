import sys
import os
import platform
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame,
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy, QComboBox
)
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QCursor, QColor


def get_light_theme(scale: float = 1.0) -> str:
    """Generate Light Theme QSS with scaled font sizes."""
    s = lambda px: int(px * scale)
    return f"""
    QWidget {{
        background-color: #F9FAFB;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: {s(14)}px;
    }}
    QLabel {{
        background: transparent;
        color: #111827;
    }}
    QLabel#headerTitle {{
        font-size: {s(28)}px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }}
    QLabel#subtitleLabel {{
        font-size: {s(14)}px;
        color: #6B7280;
    }}
    QLabel#fieldLabel {{
        font-size: {s(12)}px;
        font-weight: 700;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}
    QLabel#statusLabel {{
        font-size: {s(13)}px;
        color: #6B7280;
        font-weight: 500;
        margin-top: 8px;
    }}
    QFrame#mainCard {{
        background-color: #FFFFFF;
        border-radius: {s(16)}px;
        border: 1px solid #E5E7EB;
    }}
    QLineEdit {{
        background-color: #F3F4F6;
        border: 1px solid #D1D5DB;
        border-radius: {s(8)}px;
        padding: 0px {s(15)}px;
        min-height: {s(50)}px;
        color: #111827;
        font-size: {s(14)}px;
    }}
    QLineEdit:focus {{
        border: 2px solid #2563EB;
        background-color: #FFFFFF;
        padding: 0px {s(14)}px;
    }}
    QPushButton {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    QPushButton#primaryBtn {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3B82F6, stop:1 #1D4ED8);
        color: #FFFFFF;
        border-radius: {s(8)}px;
        padding: 0px {s(20)}px;
        min-height: {s(50)}px;
        font-size: {s(15)}px;
        font-weight: 700;
        border: none;
    }}
    QPushButton#primaryBtn:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #60A5FA, stop:1 #2563EB);
    }}
    QPushButton#primaryBtn:disabled {{
        background-color: #9CA3AF;
        color: #F3F4F6;
    }}
    QPushButton#secondaryBtn {{
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: {s(8)}px;
        padding: 0px {s(20)}px;
        min-height: {s(50)}px;
        font-size: {s(13)}px;
        font-weight: 600;
    }}
    QPushButton#secondaryBtn:hover {{
        background-color: #F3F4F6;
        color: #111827;
    }}
    QPushButton#themeBtn {{
        background-color: transparent;
        color: #4B5563;
        font-size: {s(13)}px;
        font-weight: 600;
        border-radius: {s(8)}px;
        border: 1px solid #D1D5DB;
        padding: {s(6)}px {s(12)}px;
        min-height: {s(30)}px;
    }}
    QPushButton#themeBtn:hover {{
        background-color: #E5E7EB;
        color: #111827;
    }}
    """


def get_dark_theme(scale: float = 1.0) -> str:
    """Generate Dark Theme QSS with scaled font sizes."""
    s = lambda px: int(px * scale)
    return f"""
    QWidget {{
        background-color: #111827;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: {s(14)}px;
    }}
    QLabel {{
        background: transparent;
        color: #F9FAFB;
    }}
    QLabel#headerTitle {{
        font-size: {s(28)}px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }}
    QLabel#subtitleLabel {{
        font-size: {s(14)}px;
        color: #9CA3AF;
    }}
    QLabel#fieldLabel {{
        font-size: {s(12)}px;
        font-weight: 700;
        color: #D1D5DB;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}
    QLabel#statusLabel {{
        font-size: {s(13)}px;
        color: #9CA3AF;
        font-weight: 500;
        margin-top: 8px;
    }}
    QFrame#mainCard {{
        background-color: #1F2937;
        border-radius: {s(12)}px;
        border: 1px solid #374151;
    }}
    QLineEdit {{
        background-color: #111827;
        border: 1px solid #4B5563;
        border-radius: {s(6)}px;
        padding: 0px {s(15)}px;
        min-height: {s(45)}px;
        color: #F9FAFB;
        font-size: {s(14)}px;
    }}
    QLineEdit:focus {{
        border: 2px solid #3B82F6;
        padding: 0px {s(14)}px;
    }}
    QPushButton {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    QPushButton#primaryBtn {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3B82F6, stop:1 #1D4ED8);
        color: #FFFFFF;
        border-radius: {s(8)}px;
        padding: 0px {s(20)}px;
        min-height: {s(50)}px;
        font-size: {s(15)}px;
        font-weight: 700;
        border: none;
    }}
    QPushButton#primaryBtn:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #60A5FA, stop:1 #2563EB);
    }}
    QPushButton#primaryBtn:disabled {{
        background-color: #4B5563;
        color: #9CA3AF;
    }}
    QPushButton#secondaryBtn {{
        background-color: #374151;
        color: #F9FAFB;
        border: 1px solid #4B5563;
        border-radius: {s(8)}px;
        padding: 0px {s(20)}px;
        min-height: {s(50)}px;
        font-size: {s(13)}px;
        font-weight: 600;
    }}
    QPushButton#secondaryBtn:hover {{
        background-color: #4B5563;
        border-color: #6B7280;
    }}
    QPushButton#themeBtn {{
        background-color: transparent;
        color: #D1D5DB;
        font-size: {s(13)}px;
        font-weight: 600;
        border-radius: {s(8)}px;
        border: 1px solid #4B5563;
        padding: {s(6)}px {s(12)}px;
        min-height: {s(30)}px;
    }}
    QPushButton#themeBtn:hover {{
        background-color: #374151;
        color: #FFFFFF;
    }}

    /* File Dialog Styling for Dark Mode */
    QFileDialog {{
        background-color: #1F2937;
        color: #F9FAFB;
    }}
    QFileDialog QLabel {{
        color: #F9FAFB;
    }}
    QFileDialog QLineEdit {{
        background-color: #111827;
        color: #F9FAFB;
        border: 1px solid #4B5563;
        border-radius: 4px;
        padding: 0px 8px;
        min-height: 28px;
    }}
    QFileDialog QPushButton {{
        background-color: #374151;
        color: #F9FAFB;
        border: 1px solid #4B5563;
        border-radius: 4px;
        padding: 4px 14px;
        min-height: 26px;
    }}
    QFileDialog QPushButton:hover {{
        background-color: #4B5563;
    }}
    QFileDialog QComboBox {{
        background-color: #111827;
        color: #F9FAFB;
        border: 1px solid #4B5563;
        border-radius: 4px;
        padding: 4px 8px;
        min-height: 26px;
    }}
    QFileDialog QComboBox QAbstractItemView {{
        background-color: #1F2937;
        color: #F9FAFB;
        selection-background-color: #2563EB;
    }}
    QFileDialog QTreeView, QFileDialog QListView {{
        background-color: #111827;
        color: #F9FAFB;
        border: 1px solid #4B5563;
        selection-background-color: #2563EB;
        selection-color: #FFFFFF;
    }}
    QFileDialog QHeaderView::section {{
        background-color: #1F2937;
        color: #D1D5DB;
        border: 1px solid #374151;
        padding: 4px;
    }}
    QFileDialog QToolButton {{
        background-color: #374151;
        color: #F9FAFB;
        border: 1px solid #4B5563;
        border-radius: 4px;
        padding: 4px;
    }}
    QFileDialog QToolButton:hover {{
        background-color: #4B5563;
    }}
    QFileDialog QSplitter::handle {{
        background-color: #374151;
    }}
    """


class OpenModelicaRunnerApp(QWidget):
    """
    A PyQt6 Desktop Application to run OpenModelica executables.
    Features dark/light mode, built-in zoom, robust error handling, and PEP8 compliance.
    """

    def __init__(self) -> None:
        """Initialize the application state and UI components."""
        super().__init__()
        self.is_dark_mode = True
        self.scale_factor = 1.0
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
        
        # Controls: Zoom + Theme Toggle
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Zoom Controls
        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setObjectName("themeBtn")
        self.zoom_out_btn.setMinimumSize(35, 30)
        self.zoom_out_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        self.zoom_level_label = QLabel("100%")
        self.zoom_level_label.setObjectName("fieldLabel")
        self.zoom_level_label.setMinimumWidth(50)
        self.zoom_level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setObjectName("themeBtn")
        self.zoom_in_btn.setMinimumSize(35, 30)
        self.zoom_in_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        
        # Theme Toggle
        self.theme_btn = QPushButton("☀️ Light Mode")
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        controls_layout.addWidget(self.zoom_out_btn)
        controls_layout.addWidget(self.zoom_level_label)
        controls_layout.addWidget(self.zoom_in_btn)
        controls_layout.addWidget(self.theme_btn)
        
        top_bar_layout.addLayout(titles_layout)
        top_bar_layout.addStretch()
        top_bar_layout.addLayout(controls_layout)
        
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
        
        browse_btn = QPushButton("📁 Browse")
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
        self.run_btn = QPushButton("🚀 Run Simulation")
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

    # ── Theme & Zoom ──────────────────────────────────────────────

    def toggle_theme(self) -> None:
        """Switch between dark and light themes."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def zoom_in(self) -> None:
        """Increase zoom level by 5% up to 200%."""
        if self.scale_factor < 2.0:
            self.scale_factor += 0.05
            self.zoom_level_label.setText(f"{int(self.scale_factor * 100)}%")
            self.apply_theme()

    def zoom_out(self) -> None:
        """Decrease zoom level by 5% down to 100%."""
        if self.scale_factor > 1.0:
            # Prevent floating point precision issues rounding down to 99%
            new_scale = round((self.scale_factor - 0.05) * 100) / 100.0
            if new_scale >= 1.0:
                self.scale_factor = new_scale
                self.zoom_level_label.setText(f"{int(self.scale_factor * 100)}%")
                self.apply_theme()

    def apply_theme(self) -> None:
        """Apply the CSS stylesheet corresponding to the current theme and zoom level."""
        if self.is_dark_mode:
            self.setStyleSheet(get_dark_theme(self.scale_factor))
            self.theme_btn.setText("☀️ Light Mode")
            self.shadow.setColor(QColor(0, 0, 0, 40))
        else:
            self.setStyleSheet(get_light_theme(self.scale_factor))
            self.theme_btn.setText("🌙 Dark Mode")
            self.shadow.setColor(QColor(0, 0, 0, 15))
            
        self.update_status_color()

    def update_status_color(self) -> None:
        """Update the status label color based on its text and current theme."""
        text = self.status_label.text()
        
        if "completed successfully" in text:
            bg_color = "#065F46" if self.is_dark_mode else "#D1FAE5"
            text_color = "#34D399" if self.is_dark_mode else "#065F46"
        elif "failed" in text or "Error" in text:
            bg_color = "#7F1D1D" if self.is_dark_mode else "#FEE2E2"
            text_color = "#F87171" if self.is_dark_mode else "#991B1B"
        elif "Running" in text or "Executing" in text:
            bg_color = "#1E3A8A" if self.is_dark_mode else "#DBEAFE"
            text_color = "#60A5FA" if self.is_dark_mode else "#1E40AF"
        else:
            bg_color = "#374151" if self.is_dark_mode else "#F3F4F6"
            text_color = "#D1D5DB" if self.is_dark_mode else "#4B5563"
            
        self.status_label.setStyleSheet(
            f"background-color: {bg_color}; color: {text_color}; "
            f"padding: 6px 16px; border-radius: 14px; font-weight: 600;"
        )

    # ── Input Handling ────────────────────────────────────────────

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

    # ── Validation & Execution ────────────────────────────────────

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
        """
        sim_args = ["-override", f"startTime={start_time},stopTime={stop_time}"]
        current_os = platform.system()

        if current_os == "Windows":
            program = "wsl"
            args = [exe_path] + sim_args
        else:
            if not os.access(exe_path, os.X_OK):
                os.chmod(exe_path, 0o755)
            program = exe_path
            args = sim_args

        self.run_btn.setEnabled(False)
        self.run_btn.setText("⏳ Executing Sequence...")
        self.status_label.setText(f"Running on {current_os}...")
        self.update_status_color()

        self.process = QProcess(self)
        self.process.finished.connect(self.on_process_finished)
        self.process.errorOccurred.connect(self.on_process_error)
        self.process.start(program, args)

    # ── Process Callbacks ─────────────────────────────────────────

    def on_process_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        """Handle process completion, capturing stdout/stderr."""
        self.run_btn.setEnabled(True)
        self.run_btn.setText("🚀 Run Simulation")

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
        self.run_btn.setText("🚀 Run Simulation")
        self.status_label.setText("Launch failed.")
        self.update_status_color()
        self.show_error_message("Process Error", f"Failed to start: {self.process.errorString()}")

    # ── Dialogs ───────────────────────────────────────────────────

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
            msg_box.setStyleSheet(
                "QMessageBox { background-color: #1F2937; }"
                "QLabel { color: #F9FAFB; }"
                "QPushButton { background-color: #2563EB; color: white; border-radius: 4px; padding: 6px 16px; }"
            )
        else:
            msg_box.setStyleSheet(
                "QMessageBox { background-color: #FFFFFF; }"
                "QLabel { color: #111827; }"
                "QPushButton { background-color: #2563EB; color: white; border-radius: 4px; padding: 6px 16px; }"
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = OpenModelicaRunnerApp()
    window.show()
    sys.exit(app.exec())
