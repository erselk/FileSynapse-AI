import sys
import os

# Add the parent directory to sys.path to resolve imports correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from src.core.ai_classifier import AIClassifier
    from src.core.file_analyzer import FileAnalyzer
    from src.core.folder_manager import FolderManager
except ImportError:
    # If direct import fails, try relative import
    try:
        from core.ai_classifier import AIClassifier
        from core.file_analyzer import FileAnalyzer
        from core.folder_manager import FolderManager
    except ImportError as e:
        print(f"Error importing core modules: {e}")
        print("Please make sure all required modules are installed.")
        sys.exit(1)

try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QFileDialog, QTreeView,
                           QLabel, QProgressBar, QStatusBar, QMessageBox)
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QFileSystemModel, QIcon
except ImportError as e:
    print(f"Error importing PyQt6: {e}")
    print("Please make sure PyQt6 is installed.")
    sys.exit(1)

import json
import logging

# Create logs directory if it doesn't exist
try:
    logs_dir = os.path.join(os.path.dirname(parent_dir), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
except Exception as e:
    print(f"Warning: Failed to create logs directory: {e}")

class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        
    def run(self):
        try:
            # Initialize components
            analyzer = FileAnalyzer()
            classifier = AIClassifier()
            manager = FolderManager()
            
            # Analyze files
            self.progress.emit(20)
            files_info = analyzer.scan_directory(self.folder_path)
            
            # Classify files
            self.progress.emit(40)
            categorized_files = {}
            for file_info in files_info:
                category = classifier.classify_file(file_info)
                if category not in categorized_files:
                    categorized_files[category] = []
                categorized_files[category].append(file_info)
                
            # Organize files
            self.progress.emit(60)
            results = manager.organize_files(self.folder_path, categorized_files)
            
            # Clean up empty folders
            self.progress.emit(80)
            manager.cleanup_empty_folders(self.folder_path)
            
            self.progress.emit(100)
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))
            logging.error(f"Error in worker thread: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_logging()
        self.init_ui()
        self.load_settings()
        
    def setup_logging(self):
        """Setup logging configuration."""
        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')
                
            logging.basicConfig(
                filename=os.path.join('logs', 'main.log'),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
        except Exception as e:
            # Fall back to console logging if file logging fails
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            logging.error(f"Error setting up file logging: {e}")
        
    def load_settings(self):
        """Load application settings."""
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
                
            # Apply settings
            if self.settings['theme'] == 'dark':
                self.setStyleSheet("""
                    QMainWindow {
                        background-color: #2b2b2b;
                        color: #ffffff;
                    }
                    QPushButton {
                        background-color: #0d47a1;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #1565c0;
                    }
                    QLabel {
                        color: #ffffff;
                    }
                    QTreeView {
                        background-color: #1e1e1e;
                        color: #ffffff;
                        border: 1px solid #3e3e3e;
                    }
                    QProgressBar {
                        border: 1px solid #3e3e3e;
                        border-radius: 3px;
                        text-align: center;
                    }
                    QProgressBar::chunk {
                        background-color: #0d47a1;
                    }
                    QStatusBar {
                        background-color: #1e1e1e;
                        color: #ffffff;
                    }
                """)
                
            # Set window size
            self.resize(*self.settings['ui']['window_size'])
            
        except Exception as e:
            logging.error(f"Error loading settings: {e}")
            self.settings = {
                'theme': 'dark',
                'language': 'tr',
                'ui': {
                    'window_size': [1024, 768]
                }
            }
            
    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle('FileSynapse AI')
        try:
            self.setWindowIcon(QIcon('assets/logo_256.ico'))
        except Exception as e:
            logging.warning(f"Could not set window icon: {e}")
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create folder selection area
        folder_layout = QHBoxLayout()
        self.folder_button = QPushButton('📁 Klasör Seçin')
        self.folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_button)
        
        self.start_button = QPushButton('🚀 Başlat')
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setEnabled(False)
        folder_layout.addWidget(self.start_button)
        
        layout.addLayout(folder_layout)
        
        # Create file tree view
        self.tree_view = QTreeView()
        self.file_model = QFileSystemModel()
        self.tree_view.setModel(self.file_model)
        layout.addWidget(self.tree_view)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Hazır')
        
    def select_folder(self):
        """Open folder selection dialog."""
        folder_path = QFileDialog.getExistingDirectory(self, 'Klasör Seçin')
        if folder_path:
            self.folder_path = folder_path
            self.file_model.setRootPath(folder_path)
            self.tree_view.setRootIndex(self.file_model.index(folder_path))
            self.start_button.setEnabled(True)
            self.status_bar.showMessage(f'Seçilen klasör: {folder_path}')
            logging.info(f"Selected folder: {folder_path}")
            
    def start_processing(self):
        """Start file processing."""
        try:
            # Disable buttons
            self.folder_button.setEnabled(False)
            self.start_button.setEnabled(False)
            
            # Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Create and start worker thread
            self.worker = WorkerThread(self.folder_path)
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.process_completed)
            self.worker.error.connect(self.process_error)
            self.worker.start()
            
            self.status_bar.showMessage('İşlem devam ediyor...')
            logging.info("Started processing files")
            
        except Exception as e:
            self.process_error(str(e))
            
    def update_progress(self, value):
        """Update progress bar value."""
        self.progress_bar.setValue(value)
        
    def process_completed(self, results):
        """Handle process completion."""
        # Re-enable buttons
        self.folder_button.setEnabled(True)
        self.start_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show results
        success_count = len(results.get('success', []))
        error_count = len(results.get('error', []))
        
        message = f'İşlem tamamlandı. {success_count} dosya başarıyla taşındı.'
        if error_count > 0:
            message += f' {error_count} dosyada hata oluştu.'
            
        QMessageBox.information(self, 'İşlem Tamamlandı', message)
        self.status_bar.showMessage('İşlem tamamlandı')
        logging.info(f"Process completed: {success_count} success, {error_count} errors")
        
        # Refresh file tree
        if self.settings.get('ui', {}).get('auto_refresh', True):
            self.file_model.setRootPath(self.folder_path)
            
    def process_error(self, error_message):
        """Handle process error."""
        # Re-enable buttons
        self.folder_button.setEnabled(True)
        self.start_button.setEnabled(True)
        
        # Hide progress bar
        self.progress_bar.setVisible(False)
        
        # Show error message
        QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {error_message}')
        self.status_bar.showMessage('Hata oluştu')
        logging.error(f"Process error: {error_message}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == '__main__':
    main() 