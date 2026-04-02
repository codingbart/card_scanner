"""Build script for Card Scanner .app bundle using PyInstaller."""
import PyInstaller.__main__
import os
import shutil

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TESS_BIN = '/opt/homebrew/bin/tesseract'
TESS_DATA = '/opt/homebrew/share/tessdata'

PyInstaller.__main__.run([
    os.path.join(PROJECT_DIR, 'run_desktop.py'),
    '--name=CardScanner',
    '--windowed',
    '--onedir',
    '--noconfirm',
    '--clean',
    # Include Flask templates and static files
    f'--add-data={os.path.join(PROJECT_DIR, "templates")}:templates',
    f'--add-data={os.path.join(PROJECT_DIR, "static")}:static',
    # Include tesseract binary
    f'--add-binary={TESS_BIN}:tesseract/bin',
    # Include only eng+pol tessdata
    f'--add-data={os.path.join(TESS_DATA, "eng.traineddata")}:tesseract/tessdata',
    f'--add-data={os.path.join(TESS_DATA, "pol.traineddata")}:tesseract/tessdata',
    # Hidden imports
    '--hidden-import=pytesseract',
    '--hidden-import=PIL',
    '--hidden-import=webview',
    f'--distpath={os.path.join(PROJECT_DIR, "dist")}',
    f'--workpath={os.path.join(PROJECT_DIR, "build")}',
    f'--specpath={PROJECT_DIR}',
])

# Copy tesseract dylibs into the bundle
dist_macos = os.path.join(PROJECT_DIR, 'dist', 'CardScanner.app', 'Contents', 'MacOS')
tess_bin_dir = os.path.join(dist_macos, 'tesseract', 'bin')

print('\n✓ Build complete!')
print(f'  App: {os.path.join(PROJECT_DIR, "dist", "CardScanner.app")}')
print('  Double-click CardScanner.app to run.')
