#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from sys import exit
import time
import traceback

isListenerOnLine = False
frames = []
class listennerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
    def run(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenerSocket.bind(('', 18964))
        while not self.thread_stop:
            listenerSocket.listen(1)
            listenerConn, addr = listenerSocket.accept()
            print 'connect by', addr
            try:
                msg = listenerConn.recv(1024)
            except socket.timeout:
                continue
            print msg, listenerConn
            if msg == 'start transfer':
                listenerConn.send(msg)
                while 1:
                    if len(frames) > 0:
                        try:
                            listenerConn.sendAll(frames.pop[0])
                        except:
                            break



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
while 1:
    speakerSocket.listen(1)
    conn, addr = speakerSocket.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(CHUNK*CHANNELS*2)
        if not data: break
        frames.append(data)
    conn.close()

lt.stop()
speakerSocket.close()
    
