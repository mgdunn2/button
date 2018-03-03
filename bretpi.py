from bretpiDb import bretpiDb
from brethttp import brethttp
from datetime import datetime
import time, threading

def addTime():
    db = bretpiDb()
    db.addTime(datetime.now())

def startLoop():
    threading.Timer(1, loop).start()

def loop():
    db = bretpiDb()
    http = brethttp()

    db.trySend(http.send)
    threading.Timer(10, loop).start()
