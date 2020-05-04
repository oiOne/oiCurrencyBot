"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import telebot
from bot import RUN 
from bot import STOP 
from threading import Thread
from flask import Flask
app = Flask(__name__)
import time

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def run_bot():
    while True:
        try:
            print("Running again!")
            RUN()
        except telebot.apihelper.ApiException as e:
          print(f"Error: {e}")
          STOP()
          time.sleep(5)
          print("Running again!")
          
@app.route("/startoicurrency")
def start():
    try:
        thread = Thread(target=run_bot, args=(), daemon=True)
        thread.start()
        return "Server is running"
    except:
       return "Somethong went wrong. Please try again!"


@app.route("/")
def index():
    return "Oi oi oi!"

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
