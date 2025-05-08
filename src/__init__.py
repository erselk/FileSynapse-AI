"""
FileSynapse AI
Version: 1.0.0
"""

__version__ = '1.0.0'

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
