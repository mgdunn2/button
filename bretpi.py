from bretpiDb import addTime, trySend
from brethttp import send
from datetime import datetime
import time, threading

def addTime():
    addTime(datetime.now())

def startLoop():
    threading.Timer(1, loop).start()

def loop():
    trySend(send)
    threading.Timer(10, loop).start()
