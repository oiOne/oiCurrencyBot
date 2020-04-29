"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from bot import RUN 
from threading import Thread
from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/hello')
def hello():
    return "Hello!"

@app.route("/startoicurrency")
def start():
    try:
        thread = Thread(target=RUN, args=(), daemon=True)
        thread.start()
        return "Server is running"
    except:
       return "Somethong went wrong. Please try again!"


@app.route("/healthcheck")
def healthCheck():
    return "Check check"

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
