from app import init_app
import threading
import requests
import time

application = init_app()

def keep_alive():
    while True:
        try:
            requests.get("https://ccrayp.onrender.com/api/post/list")
        except Exception as e:
            print("База данных уснула")
        time.sleep(299)

if __name__ != "__main__":
    t = threading.Thread(target=keep_alive)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    application.run(port=8000)
