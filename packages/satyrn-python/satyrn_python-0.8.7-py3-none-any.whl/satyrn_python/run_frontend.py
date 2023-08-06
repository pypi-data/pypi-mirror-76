import getopt
import multiprocessing
import os
import sys
import time
import webbrowser

from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

from .app import create_app
from .interpreter import Interpreter

interpreter = Interpreter()
client_instance = 0

arguments = sys.argv[1:]

opts, args = getopt.getopt(arguments, "hi:o:", ["port=", "hidden"])

url = "0.0.0.0"
port = 20787

for opt, arg in opts:
    if opt == "--port":
        port = int(arg)
    if opt == "--hidden":
        url = "127.0.0.1"


openurl = "localhost" if url == "0.0.0.0" else url


def delayed_browser_open():
    time.sleep(3)

    webbrowser.open("http://" + openurl + ":" + str(port) + "/#loaded")


def run_frontend():
    with open(os.path.abspath(__file__)[:(-1 * len(os.path.splitext(__file__)[0]))] + "/asciiart.txt") as asciiart:
        print("".join(asciiart.readlines()))

    print("Thank you for using Satyrn! For issues and updates visit https://GitHub.com/CharlesAverill/satyrn\n")

    print("Initializing CherryPy server...")

    os.environ["FLASK_APP"] = "satyrnUI.satyrnUI"
    os.environ["FLASK_ENV"] = "production"

    d = PathInfoDispatcher({'/': create_app(interpreter, client_instance)})
    server = WSGIServer((url, port), d)

    try:
        p = multiprocessing.Process(target=delayed_browser_open)
        p.start()

        print("Hosting at http://" + openurl + ":" + str(port) + "/#loaded")

        server.start()
    except KeyboardInterrupt:
        print("Stopping CherryPy server...")
        server.stop()
        print("Stopped")


if __name__ == "__main__":
    run_frontend()
