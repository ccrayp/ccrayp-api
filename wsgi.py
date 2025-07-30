from app import init_app
import threading
import requests
import time

application = init_app()

def keep_alive():
    while True:
        try:
            requests.get("https://ccrayp.onrender.com/api/ping")
            print("✅ Self-ping sent to /api/ping")
        except Exception as e:
            print(f"❌ Self-ping failed: {e}")
        time.sleep(300)

if __name__ != "__main__":
    t = threading.Thread(target=keep_alive)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    application.run(port=8000)