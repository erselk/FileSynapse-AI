import os
import shutil
from datetime import datetime
import logging

class FolderManager:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')
                
            logging.basicConfig(
                filename=os.path.join('logs', 'folder_manager.log'),
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
        
    def organize_files(self, base_path, categorized_files):
        """Organize files into categories."""
        results = {'success': [], 'error': []}
        
        try:
            # Create category folders
            for category in categorized_files.keys():
                category_path = os.path.join(base_path, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    logging.info(f"Created category folder: {category_path}")
                    
            # Move files to their respective categories
            for category, files in categorized_files.items():
                category_path = os.path.join(base_path, category)
                
                for file_info in files:
                    try:
                        source_path = file_info['path']
                        filename = os.path.basename(source_path)
                        target_path = os.path.join(category_path, filename)
                        
                        # Handle file name conflicts
                        if os.path.exists(target_path):
                            base, ext = os.path.splitext(filename)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            target_path = os.path.join(category_path, f"{base}_{timestamp}{ext}")
                            
                        # Move the file
                        shutil.move(source_path, target_path)
                        results['success'].append(source_path)
                        logging.info(f"Moved file: {source_path} -> {target_path}")
                        
                    except Exception as e:
                        results['error'].append(source_path)
                        logging.error(f"Error moving file {source_path}: {e}")
                        
        except Exception as e:
            logging.error(f"Error organizing files: {e}")
            
        return results
        
    def create_folder_structure(self, base_path, structure):
        """Create a folder structure based on a dictionary."""
        try:
            for folder, subfolders in structure.items():
                folder_path = os.path.join(base_path, folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    logging.info(f"Created folder: {folder_path}")
                    
                if isinstance(subfolders, dict):
                    self.create_folder_structure(folder_path, subfolders)
                    
            return True
            
        except Exception as e:
            logging.error(f"Error creating folder structure: {e}")
            return False
            
    def move_file(self, source, target, overwrite=False):
        """Move a file from source to target path."""
        try:
            # Create target directory if it doesn't exist
            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                
            # Handle existing files
            if os.path.exists(target):
                if overwrite:
                    os.remove(target)
                else:
                    base, ext = os.path.splitext(target)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    target = f"{base}_{timestamp}{ext}"
                    
            # Move the file
            shutil.move(source, target)
            logging.info(f"Moved file: {source} -> {target}")
            return True
            
        except Exception as e:
            logging.error(f"Error moving file {source}: {e}")
            return False
            
    def cleanup_empty_folders(self, path):
        """Remove empty folders recursively."""
        removed = []
        try:
            for root, dirs, files in os.walk(path, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        if not os.listdir(dir_path):  # Check if directory is empty
                            os.rmdir(dir_path)
                            removed.append(dir_path)
                            logging.info(f"Removed empty folder: {dir_path}")
                    except Exception as e:
                        logging.error(f"Error removing folder {dir_path}: {e}")
                        
        except Exception as e:
            logging.error(f"Error cleaning up empty folders: {e}")
            
        return removed
        
    def undo_move(self, move_history):
        """Undo file moves based on history."""
        results = {'success': [], 'error': []}
        
        for move in move_history:
            try:
                source = move['target']
                target = move['source']
                
                if os.path.exists(source):
                    # Create target directory if needed
                    target_dir = os.path.dirname(target)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        
                    # Move file back
                    shutil.move(source, target)
                    results['success'].append(source)
                    logging.info(f"Undid move: {source} -> {target}")
                else:
                    results['error'].append(source)
                    logging.error(f"Source file not found: {source}")
                    
            except Exception as e:
                if 'source' in locals():
                    results['error'].append(source)
                logging.error(f"Error undoing move: {e}")
                
        return results
            
    def create_backup(self, path):
        """Create a backup of the directory."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{path}_backup_{timestamp}"
            
            shutil.copytree(path, backup_path)
            logging.info(f"Created backup: {backup_path}")
            
            return backup_path
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            return None
            
    def restore_backup(self, backup_path, original_path):
        """Restore from a backup."""
        try:
            if os.path.exists(original_path):
                shutil.rmtree(original_path)
            
            shutil.copytree(backup_path, original_path)
            logging.info(f"Restored from backup: {backup_path} -> {original_path}")
            return True
        except Exception as e:
            logging.error(f"Error restoring backup: {e}")
            return False
            
    def get_file_info(self, path):
        """Get file information."""
        try:
            stat = os.stat(path)
            return {
                'path': path,
                'name': os.path.basename(path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'extension': os.path.splitext(path)[1].lower()
            }
        except Exception as e:
            logging.error(f"Error getting file info for {path}: {e}")
            return None 