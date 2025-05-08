import os
import json
import re
import mimetypes
import logging
from datetime import datetime
import random

class AIClassifier:
    def __init__(self):
        self.setup_logging()
        self.load_category_mappings()
        
    def setup_logging(self):
        """Setup logging configuration."""
        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')
                
            logging.basicConfig(
                filename=os.path.join('logs', 'ai_classifier.log'),
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
        
    def load_category_mappings(self):
        """Load category mappings from JSON file."""
        try:
            with open('category_mappings.json', 'r', encoding='utf-8') as f:
                self.category_mappings = json.load(f)
            logging.info("Category mappings loaded successfully")
        except Exception as e:
            logging.error(f"Error loading category mappings: {e}")
            # Fallback mappings if file is missing
            self.category_mappings = {
                "document": {
                    "name": "Belgeler",
                    "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx"],
                    "mime_types": ["application/pdf", "application/msword", "text/plain"]
                },
                "media": {
                    "name": "Medya",
                    "extensions": [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mp3", ".wav"],
                    "mime_types": ["image/", "video/", "audio/"]
                },
                "code": {
                    "name": "Kod",
                    "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
                    "mime_types": ["text/x-python", "application/javascript", "text/html"]
                },
                "design": {
                    "name": "Tasarım",
                    "extensions": [".psd", ".ai", ".svg", ".sketch", ".fig", ".xd"],
                    "mime_types": ["image/vnd.adobe.photoshop", "application/postscript", "image/svg+xml"]
                },
                "archive": {
                    "name": "Arşiv",
                    "extensions": [".zip", ".rar", ".7z", ".tar", ".gz"],
                    "mime_types": ["application/zip", "application/x-rar-compressed", "application/x-7z-compressed"]
                },
                "other": {
                    "name": "Diğer",
                    "extensions": [],
                    "mime_types": []
                }
            }
            
    def classify_file(self, file_info):
        """Classify a file based on its metadata and content."""
        try:
            # Get basic classifications
            ext_category = self._classify_by_extension(file_info['extension'])
            mime_category = self._classify_by_mime(file_info['mime_type'])
            name_category = self._classify_by_name(file_info['name'])
            
            # Priority-based classification (extension > mime > name)
            if ext_category != "other":
                final_category = ext_category
            elif mime_category != "other":
                final_category = mime_category
            elif name_category != "other":
                final_category = name_category
            else:
                final_category = "other"
                
            logging.info(f"File classified as: {final_category}")
            return final_category
            
        except Exception as e:
            logging.error(f"Error classifying file: {e}")
            return "other"
            
    def _classify_by_extension(self, extension):
        """Classify file by its extension."""
        extension = extension.lower()
        for category, info in self.category_mappings.items():
            if 'extensions' in info and extension in info['extensions']:
                return category
        return "other"
        
    def _classify_by_mime(self, mime_type):
        """Classify file by its MIME type."""
        for category, info in self.category_mappings.items():
            if 'mime_types' in info:
                for mime_pattern in info['mime_types']:
                    if mime_type.startswith(mime_pattern):
                        return category
        return "other"
    
    def _classify_by_name(self, filename):
        """Classify file by keywords in its name."""
        filename = filename.lower()
        
        for category, info in self.category_mappings.items():
            if 'keywords' in info:
                for keyword in info['keywords']:
                    if keyword.lower() in filename:
                        return category
        
        return "other"
    
    def batch_classify(self, files_info):
        """Classify multiple files and group them by category."""
        categorized = {}
        
        # Initialize categories from mappings
        for category in self.category_mappings.keys():
            categorized[category] = []
        
        # Classify each file
        for file_info in files_info:
            category = self.classify_file(file_info)
            categorized[category].append(file_info)
            
        return categorized
        
    def update_category_mappings(self, new_mappings):
        """Update category mappings with user-provided data."""
        self.category_mappings.update(new_mappings)
        
        # Save to file
        try:
            with open('category_mappings.json', 'w', encoding='utf-8') as f:
                json.dump(self.category_mappings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Error saving category mappings: {e}")

# Test the class if this file is run directly
if __name__ == "__main__":
    classifier = AIClassifier()
    test_file = {
        'name': 'test_document.pdf',
        'extension': '.pdf',
        'mime_type': 'application/pdf',
        'size': 1024
    }
    category = classifier.classify_file(test_file)
    print(f"Test file classified as: {category}") 