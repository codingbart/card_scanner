from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from ocr_engine import extract_text
from parser import parse_card_text
from csv_handler import append_contact
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import os
import sys


def _get_resource_dir():
    """In PyInstaller bundle, resources are in _MEIPASS. Otherwise use script dir."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


_res = _get_resource_dir()
app = Flask(__name__,
            template_folder=os.path.join(_res, 'templates'),
            static_folder=os.path.join(_res, 'static'))
app.secret_key = 'card-scanner-secret-key'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def scan():
    file = request.files.get('card_image')
    if not file or not allowed_file(file.filename):
        flash('Prześlij prawidłowy plik obrazu (PNG, JPG, BMP, TIFF, WEBP).', 'error')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        raw_text = extract_text(filepath)
        parsed = parse_card_text(raw_text)
    finally:
        os.remove(filepath)

    return render_template('result.html', data=parsed, raw_text=raw_text)


@app.route('/save', methods=['POST'])
def save():
    data = {
        'name': request.form.get('name', '').strip(),
        'surname': request.form.get('surname', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'company': request.form.get('company', '').strip(),
        'position': request.form.get('position', '').strip(),
        'website': request.form.get('website', '').strip(),
    }
    append_contact(data)
    flash('Kontakt zapisany!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
