#!/usr/bin/env python
"""
FileSynapse AI Launcher Script
This script ensures that the application can find all its dependencies
"""

import os
import sys
import traceback

def show_error_message(error_message):
    """Display an error message in a GUI window if possible"""
    try:
        # First try to use PyQt for a nice error dialog
        from PyQt6.QtWidgets import QApplication, QMessageBox
        app = QApplication([])
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("FileSynapse AI - Hata")
        msg.setText("Uygulama başlatılırken bir hata oluştu:")
        msg.setDetailedText(error_message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    except ImportError:
        # If PyQt is not available, just print to console
        print(f"Error loading application: {error_message}")
        print("Make sure all dependencies are installed:")
        print("1. Run: pip install -r requirements.txt")
        print("\nIf problems persist, try building the application again using build_fix.bat")
        try:
            input("Press Enter to exit...")
        except:
            pass

# Add the current directory to Python's path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Make sure stderr and stdout are properly redirected
try:
    sys.stdout = open(os.path.join(current_dir, 'logs', 'stdout.log'), 'w')
    sys.stderr = open(os.path.join(current_dir, 'logs', 'stderr.log'), 'w')
except:
    # If we can't create log files, continue anyway
    pass

# Create logs directory if it doesn't exist
try:
    os.makedirs(os.path.join(current_dir, 'logs'), exist_ok=True)
except:
    pass

try:
    # Import the main module from src
    from src.main import main
    
    # Run the application
    if __name__ == "__main__":
        sys.exit(main())
except Exception as e:
    # Get the full error message with traceback
    error_message = traceback.format_exc()
    
    # Show error message
    show_error_message(error_message)
    sys.exit(1) 