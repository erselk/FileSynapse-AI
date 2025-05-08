from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar,
    QTreeWidget, QTreeWidgetItem, QMessageBox, QTabWidget,
    QComboBox, QCheckBox, QSpinBox, QGroupBox, QStyleFactory
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from typing import Dict, List
import os

class ScanWorker(QThread):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int)
    
    def __init__(self, file_analyzer, ai_classifier, path):
        super().__init__()
        self.file_analyzer = file_analyzer
        self.ai_classifier = ai_classifier
        self.path = path
        
    def run(self):
        # Scan files
        files_info = self.file_analyzer.scan_directory(self.path)
        self.progress.emit(50)
        
        # Classify files
        categorized = self.ai_classifier.batch_classify(files_info)
        self.progress.emit(100)
        
        self.finished.emit(categorized)

class MainWindow(QMainWindow):
    def __init__(self, file_analyzer, ai_classifier, folder_manager):
        super().__init__()
        self.file_analyzer = file_analyzer
        self.ai_classifier = ai_classifier
        self.folder_manager = folder_manager
        
        self.setWindowTitle("FileSynapse AI - Akıllı Dosya Düzenleme Sistemi")
        self.setMinimumSize(800, 600)
        
        self.init_ui()
        
    def init_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create top buttons
        top_layout = QHBoxLayout()
        
        self.select_folder_btn = QPushButton("📁 Klasör Seçin")
        self.select_folder_btn.clicked.connect(self.select_folder)
        top_layout.addWidget(self.select_folder_btn)
        
        self.start_btn = QPushButton("🚀 Başlat")
        self.start_btn.clicked.connect(self.start_scan)
        self.start_btn.setEnabled(False)
        top_layout.addWidget(self.start_btn)
        
        layout.addLayout(top_layout)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Create tree widget for results
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Dosya", "Kategori", "Boyut"])
        layout.addWidget(self.tree)
        
        # Create bottom buttons
        bottom_layout = QHBoxLayout()
        
        self.undo_btn = QPushButton("↩️ Geri Al")
        self.undo_btn.clicked.connect(self.undo_last)
        self.undo_btn.setEnabled(False)
        bottom_layout.addWidget(self.undo_btn)
        
        self.apply_btn = QPushButton("✅ Uygula")
        self.apply_btn.clicked.connect(self.apply_changes)
        self.apply_btn.setEnabled(False)
        bottom_layout.addWidget(self.apply_btn)
        
        layout.addLayout(bottom_layout)
        
        # Initialize variables
        self.selected_path = None
        self.categorized_files = None
        
    def select_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Klasör Seçin")
        if path:
            self.selected_path = path
            self.start_btn.setEnabled(True)
            
    def start_scan(self):
        if not self.selected_path:
            return
            
        # Clear previous results
        self.tree.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Disable buttons during scan
        self.start_btn.setEnabled(False)
        self.select_folder_btn.setEnabled(False)
        
        # Start scan in background
        self.scan_worker = ScanWorker(self.file_analyzer, self.ai_classifier, self.selected_path)
        self.scan_worker.progress.connect(self.update_progress)
        self.scan_worker.finished.connect(self.scan_finished)
        self.scan_worker.start()
        
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def scan_finished(self, categorized_files):
        self.categorized_files = categorized_files
        self.progress_bar.setVisible(False)
        
        # Populate tree with results
        for category, files in categorized_files.items():
            if not files:
                continue
                
            category_item = QTreeWidgetItem(self.tree)
            category_item.setText(0, self.folder_manager.category_folders[category])
            
            for file_info in files:
                file_item = QTreeWidgetItem(category_item)
                file_item.setText(0, file_info['name'])
                file_item.setText(1, category)
                file_item.setText(2, f"{file_info['size'] / 1024:.1f} KB")
                
        self.tree.expandAll()
        
        # Enable buttons
        self.start_btn.setEnabled(True)
        self.select_folder_btn.setEnabled(True)
        self.apply_btn.setEnabled(True)
        
    def apply_changes(self):
        if not self.categorized_files:
            return
            
        reply = QMessageBox.question(
            self,
            "Onay",
            "Dosyaları düzenlemek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Create folder structure
            created_folders = self.folder_manager.create_folder_structure(
                self.selected_path,
                self.categorized_files
            )
            
            # Move files
            moved_files = self.folder_manager.move_files(
                self.categorized_files,
                created_folders
            )
            
            # Show success message
            QMessageBox.information(
                self,
                "Başarılı",
                f"{len(moved_files)} dosya başarıyla düzenlendi."
            )
            
            # Enable undo button
            self.undo_btn.setEnabled(True)
            
    def undo_last(self):
        if self.folder_manager.undo_last_operation():
            QMessageBox.information(
                self,
                "Başarılı",
                "Son işlem geri alındı."
            )
        else:
            QMessageBox.warning(
                self,
                "Hata",
                "Geri alınacak işlem bulunamadı."
            ) 