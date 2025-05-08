import os
import mimetypes
import logging
from datetime import datetime
import re

# Initialize mimetypes
mimetypes.init()

class FileAnalyzer:
    """
    A class to analyze files and extract useful information
    """
    
    def __init__(self):
        """
        Initialize the FileAnalyzer with common file extensions and MIME types
        """
        self.setup_logging()
        
        # Dictionary to store common file types and their extensions
        self.file_extensions = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.mp4': 'video/mp4',
            '.mp3': 'audio/mpeg',
            '.psd': 'image/vnd.adobe.photoshop',
            '.ai': 'application/illustrator',
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed',
            '.exe': 'application/x-msdownload',
            '.py': 'text/x-python',
            '.js': 'application/javascript',
            '.html': 'text/html',
            '.css': 'text/css',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        }
        
        # Regular expressions for extracting information from filenames
        self.version_regex = re.compile(r'v(\d+(\.\d+)*)|version\s*(\d+(\.\d+)*)', re.IGNORECASE)
        self.draft_regex = re.compile(r'draft|taslak', re.IGNORECASE)
        self.final_regex = re.compile(r'final|son', re.IGNORECASE)
    
    def setup_logging(self):
        """Setup logging configuration."""
        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')
                
            logging.basicConfig(
                filename=os.path.join('logs', 'file_analyzer.log'),
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
        
    def scan_directory(self, directory_path):
        """
        Scan a directory and return information about all files
        
        Args:
            directory_path (str): Path to the directory to scan
            
        Returns:
            list: List of dictionaries with file information
        """
        logging.info(f"Scanning directory: {directory_path}")
        
        files_info = []
        
        try:
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    # Get file information
                    file_info = self.analyze_file(file_path)
                    
                    if file_info:
                        files_info.append(file_info)
                        
        except Exception as e:
            logging.error(f"Error scanning directory: {e}")
            
        logging.info(f"Found {len(files_info)} files")
        return files_info
    
    def analyze_file(self, file_path):
        """
        Analyze a file and extract information
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: Dictionary with file information
        """
        try:
            # Skip files that don't exist or are too large
            if not os.path.exists(file_path) or os.path.getsize(file_path) > 100 * 1024 * 1024:  # Skip files > 100MB
                return None
            
            # Basic file information
            filename = os.path.basename(file_path)
            file_extension = os.path.splitext(filename)[1].lower()
            file_size = os.path.getsize(file_path)
            
            # Get file modification time
            modification_time = os.path.getmtime(file_path)
            modified_date = datetime.fromtimestamp(modification_time)
            
            # Get file creation time
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(creation_time)
            
            # Get MIME type
            mime_type = self.get_mime_type(file_path)
            
            # Extract version information from filename
            version_info = self.extract_version_info(filename)
            
            # Create file information dictionary
            file_info = {
                'path': file_path,
                'name': filename,
                'extension': file_extension,
                'size': file_size,
                'modified_date': modified_date,
                'creation_date': creation_date,
                'mime_type': mime_type,
                'version_info': version_info
            }
            
            # Add file content analysis if possible
            if file_size < 10 * 1024 * 1024:  # Only analyze files < 10MB
                keywords = self.extract_keywords(file_path, mime_type)
                file_info['keywords'] = keywords
            
            return file_info
            
        except Exception as e:
            logging.error(f"Error analyzing file {file_path}: {e}")
            return None
    
    def get_mime_type(self, file_path):
        """
        Get the MIME type of a file using file extension
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: MIME type of the file
        """
        try:
            # Get file extension
            extension = os.path.splitext(file_path)[1].lower()
            
            # If extension is in our dictionary, return the MIME type
            if extension in self.file_extensions:
                return self.file_extensions[extension]
            
            # Otherwise, try to guess using mimetypes
            mime_type, _ = mimetypes.guess_type(file_path)
            
            # If mimetypes failed, use a default based on the extension
            if mime_type is None:
                if extension:
                    mime_type = f"application/{extension[1:]}"
                else:
                    mime_type = "application/octet-stream"
            
            return mime_type
        
        except Exception as e:
            logging.error(f"Error getting MIME type for {file_path}: {e}")
            return "application/octet-stream"
    
    def extract_version_info(self, filename):
        """
        Extract version information from a filename
        
        Args:
            filename (str): Name of the file
            
        Returns:
            dict: Dictionary with version information
        """
        # Initialize version info
        version_info = {
            'is_version': False,
            'version_number': None,
            'is_draft': False,
            'is_final': False
        }
        
        # Check for version number
        version_match = self.version_regex.search(filename)
        if version_match:
            version_info['is_version'] = True
            version_info['version_number'] = version_match.group(1) or version_match.group(3)
        
        # Check for draft/final status
        if self.draft_regex.search(filename):
            version_info['is_draft'] = True
        
        if self.final_regex.search(filename):
            version_info['is_final'] = True
        
        return version_info
    
    def extract_keywords(self, file_path, mime_type):
        """
        Extract keywords from a file's content
        
        Args:
            file_path (str): Path to the file
            mime_type (str): MIME type of the file
            
        Returns:
            list: List of keywords
        """
        keywords = []
        
        try:
            # For text files
            if mime_type.startswith('text/') or mime_type in ['application/pdf', 'application/msword', 
                                                              'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                # Read the first 1000 bytes as text
                with open(file_path, 'rb') as f:
                    content = f.read(1000)
                
                # Try to decode as UTF-8, ignore errors
                try:
                    text = content.decode('utf-8', errors='ignore')
                    # Simple keyword extraction - just split by spaces and filter
                    words = [word.lower() for word in re.findall(r'\b\w+\b', text) if len(word) > 3]
                    keywords = list(set(words))[:20]  # Take up to 20 unique keywords
                except Exception:
                    pass
        
        except Exception as e:
            logging.error(f"Error extracting keywords from {file_path}: {e}")
        
        return keywords


# Test the class if this file is run directly
if __name__ == "__main__":
    analyzer = FileAnalyzer()
    test_dir = os.path.expanduser("~/Documents")
    files = analyzer.scan_directory(test_dir)
    for file in files[:5]:  # Print first 5 files for testing
        print(f"File: {file['name']}")
        print(f"  MIME Type: {file['mime_type']}")
        print(f"  Size: {file['size']} bytes")
        print() 