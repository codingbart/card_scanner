import webview
import threading
from app import app


def start_flask():
    app.run(port=5000, use_reloader=False)


if __name__ == '__main__':
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()
    webview.create_window('Business Card Scanner', 'http://127.0.0.1:5000',
                          width=700, height=800)
    webview.start()
