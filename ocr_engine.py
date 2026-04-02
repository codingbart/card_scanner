import os
import sys
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance


def _configure_tesseract():
    """Point pytesseract to bundled tesseract binary when running from .app bundle."""
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        tess_bin = os.path.join(bundle_dir, 'tesseract', 'bin', 'tesseract')
        tess_data = os.path.join(bundle_dir, 'tesseract', 'tessdata')
        if os.path.exists(tess_bin):
            pytesseract.pytesseract.tesseract_cmd = tess_bin
            os.environ['TESSDATA_PREFIX'] = tess_data


_configure_tesseract()


def preprocess(image: Image.Image) -> Image.Image:
    """Improve OCR accuracy on business cards."""
    img = image.convert('L')
    img = img.filter(ImageFilter.MedianFilter(3))
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    img = img.point(lambda x: 0 if x < 140 else 255)
    return img


def extract_text(image_path: str) -> str:
    img = Image.open(image_path)
    img = preprocess(img)
    text = pytesseract.image_to_string(img, lang='eng+pol')
    return text
