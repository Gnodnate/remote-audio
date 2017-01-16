#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from sys import exit
import time
import traceback

msgSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msgSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
msgSocket.bind(('', 18964))

isListenerOnLine = False

class listennerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
    def run(self):
        while not self.thread_stop:
            global listenerConn
            listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listenerSocket.bind('', 18964)
            listenerSocket.listen(1)
            listenerConn, addr = listenerSocket.accept()
            try:
                msg = msgSocket.recv(1024)
            except socket.timeout:
                continue
            print msg, listenerConn
            if msg == 'start transfer':
                isListenerOnLine = True
                msgSocket.send(msg)
            if msg == 'quit transfer':
                isListenerOnLine = False

    def stop(self):
        self.thread_stop = True

lT = listennerThread()
lT.setDaemon(True)
lT.start()

SPORT = 18965
CHUNK = 1024
CHANNELS = 1

speakerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
speakerSocket.bind(('', SPORT))
speakerSocket.listen(1)
conn, addr = speakerSocket.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(CHUNK*CHANNELS*2)
    if not data: break
    listenerConn.sendall(data)
conn.close()

lt.stop()
speakerSocket.close()
    
