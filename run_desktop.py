import multiprocessing
import webview
import threading
import time
import urllib.request
from app import app


def start_flask():
    app.run(port=5000, use_reloader=False)


def wait_for_flask(url='http://127.0.0.1:5000', timeout=10):
    """Wait until Flask server is ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url)
            return True
        except Exception:
            time.sleep(0.1)
    return False


if __name__ == '__main__':
    multiprocessing.freeze_support()

    t = threading.Thread(target=start_flask, daemon=True)
    t.start()

    wait_for_flask()

    webview.create_window('Business Card Scanner', 'http://127.0.0.1:5000',
                          width=700, height=800)
    webview.start()
