from app import init_app
import threading
import requests
import time

application = init_app()

if __name__ == '__main__':
    application.run(port=8000)
