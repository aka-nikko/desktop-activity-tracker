"""
This script sets up a system tray icon for the Desktop Activity Tracker application.
It allows users to start and stop tracking, summarize the day's activity, and access configuration files.
"""

import os
import threading
import multiprocessing
import subprocess
from pathlib import Path
from PIL import Image
from pystray import Icon, Menu, MenuItem
import tkinter as tk
from tkinter import messagebox
from main import run_tracker
from config.load_config import resource_path, config_path, env_path

# Initialize logger
main_logger = None
def get_logger():
    """Get the main logger instance, initializing it if necessary."""
    global main_logger
    if main_logger is None:
        from logging_utils.logger import init_logger
        main_logger = init_logger("TRAY", is_main=True)
    return main_logger

class TrayApp:
    """
    TrayApp encapsulates all system tray functionality and manages the tracker process.
    """
    def __init__(self) -> None:
        # Queue for inter-process communication with the tracker
        self.cmd_queue = multiprocessing.Queue()
        self.tracker_process = None

        # Initialize system tray icon
        self.icon = self._create_icon()

    def show_dialog(self, title: str, message: str, dialog_type: str = "info") -> None:
        """Show a dialog box with the specified title and message."""
        def _show():
            root = tk.Tk()
            root.withdraw()
            dlg_map = {
                "info": messagebox.showinfo,
                "warning": messagebox.showwarning,
                "error": messagebox.showerror,
                "question": messagebox.askquestion
            }
            func = dlg_map.get(dialog_type.lower(), messagebox.showinfo)
            func(title, message)
            root.quit()
            root.destroy()

        threading.Thread(target=_show).start()

    def _create_icon(self):
        """Set up the tray icon and its menu."""
        icon = Icon("ActivityTracker")
        try:
            icon.icon = Image.open(resource_path("assets/icon.ico"))
        except Exception as e:
            get_logger().error(f"Failed to load tray icon: {e}")
            icon.icon = None

        icon.menu = Menu(
            MenuItem("Start Tracking", self.start_tracking),
            MenuItem("Stop Tracking", self.stop_tracking),
            MenuItem("Summarize", self.summarize),
            MenuItem("OpenAI API Key", self.open_env),
            MenuItem("Settings", self.open_config),
            MenuItem("Exit", self.quit_app)
        )
        icon.title = "Desktop Activity Tracker"
        return icon

    def start_tracking(self, icon, item) -> None:
        """Start the tracker process if not already running."""
        if self.tracker_process is None or not self.tracker_process.is_alive():
            self.tracker_process = multiprocessing.Process(
                target=run_tracker, args=(self.cmd_queue,), daemon=True
            )
            self.tracker_process.start()
            get_logger().info("Tracking started.")
            self.show_dialog("Tracking Started", "Activity Tracker is now running.")
        else:
            get_logger().warning("Tracker is already running.")
            self.show_dialog("Already Running", "Activity Tracker is already in progress.", "warning")

    def stop_tracking(self, icon, item) -> None:
        """Stop the tracker process if it is running."""
        if self.tracker_process and self.tracker_process.is_alive():
            self.tracker_process.terminate()
            self.tracker_process.join()
            self.tracker_process = None
            get_logger().info("Tracking stopped.")
            self.show_dialog("Tracking Stopped", "Activity Tracker has been stopped.")
        else:
            get_logger().warning("Tracker is not running.")
            self.show_dialog("Not Running", "Activity Tracker is not currently running.", "warning")

    def summarize(self, icon, item) -> None:
        """Send a command to the tracker process to summarize the day."""
        if self.tracker_process and self.tracker_process.is_alive():
            self.cmd_queue.put("summarize")
            get_logger().info("Sent 'summarize' command.")
            self.show_dialog("Summarize Command Sent", "The tracker will summarize the day's activity.")

    def open_file(self, path: Path) -> None:
        """Open a file with the default system editor."""
        try:
            if os.name == "nt":  # Windows
                os.startfile(path)
            elif os.name == "posix":
                subprocess.call(["xdg-open", str(path)])  # Linux
            else:
                subprocess.call(["open", str(path)])  # macOS
        except Exception as e:
            get_logger().error(f"Could not open file: {e}")

    def open_env(self, icon, item) -> None:
        """Open the .env file for editing."""
        self.open_file(env_path)

    def open_config(self, icon, item) -> None:
        """Open the settings configuration file."""
        self.open_file(config_path)

    def quit_app(self, icon, item) -> None:
        """Quit the application and stop the tracker if running."""
        # Silently stop tracking without dialogs
        if self.tracker_process and self.tracker_process.is_alive():
            self.tracker_process.terminate()
            self.tracker_process.join()
            self.tracker_process = None
            get_logger().info("Tracking stopped (via exit).")
        icon.stop()
        get_logger().info("Application exited.")
        self.show_dialog("Exiting", "Desktop Activity Tracker is exiting.")

    def run(self) -> threading.Thread:
        """Start the tray icon in a background thread."""
        tray_thread = threading.Thread(target=self.icon.run)
        tray_thread.start()
        get_logger().info("Tray icon is running...")
        self.show_dialog("Tray Started", "Desktop Activity Tracker is running in the system tray.")
        return tray_thread

if __name__ == "__main__":
    # Required for Windows to prevent multiprocessing issues on script re-import
    multiprocessing.freeze_support()

    # Create and start the tray app
    app = TrayApp()
    tray_thread = app.run()

    # Wait for tray to finish (i.e., exit selected)
    tray_thread.join()
    get_logger().info("Script has fully exited.")
