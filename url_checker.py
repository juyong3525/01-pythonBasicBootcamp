import requests
import threading

URL = "http://www.hanflower.com/"


def server_status():
    try:
        response = requests.get(URL)
        status = response.status_code
        print(status)
    except:
        print("No connection")
    threading.Timer(10, server_status).start()


server_status()
