import os
import sys


def get_base_dir():
    """Handle both normal run and PyInstaller frozen bundle."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
CSV_PATH = os.path.join(BASE_DIR, 'output', 'contacts.csv')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'}
