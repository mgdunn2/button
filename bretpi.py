from bretpiDb import addTime, trySend
from brethttp import send
from datetime import datetime
import time, threading

def addNewTime():
    addTime(datetime.now())

def startSendLoop():
    threading.Timer(1, sendLoop).start()

def sendLoop():
    trySend(send)
    threading.Timer(10, sendLoop).start()
