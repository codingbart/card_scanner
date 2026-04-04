import multiprocessing
import sys
import threading
import time
import urllib.request
import webbrowser
from app import app

URL = 'http://127.0.0.1:5000'


def start_flask():
    app.run(port=5000, use_reloader=False)


def wait_for_flask(timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(URL)
            return True
        except Exception:
            time.sleep(0.1)
    return False


def run_with_webview():
    import webview
    webview.create_window('Business Card Scanner', URL, width=700, height=800)
    webview.start()


def run_with_browser():
    webbrowser.open(URL)
    print(f'CardScanner dziala na {URL}')
    print('Zamknij to okno aby zakonczyc.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    multiprocessing.freeze_support()

    t = threading.Thread(target=start_flask, daemon=True)
    t.start()
    wait_for_flask()

    if sys.platform == 'win32':
        run_with_browser()
    else:
        try:
            run_with_webview()
        except Exception:
            run_with_browser()
