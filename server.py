#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from sys import exit
import time
import traceback

frames = []
isThereListener = False
class listennerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
    def run(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenerSocket.bind(('', 18964))
        while not self.thread_stop:
            print 'waiting for listener'
            listenerSocket.listen(1)
            listenerConn, addr = listenerSocket.accept()
            listenerConn.settimeout(5)
            try:
                msg = listenerConn.recv(1024)
            except socket.timeout:
                continue
            if msg == 'start transfer':
                global isThereListener
                isThereListener = True
                print 'get listener at', addr, isThereListener

                listenerConn.send(msg)
                count = 0
                while 1:
                    if len(frames) > 0:
                        try:
                            listenerConn.sendall(frames.pop(0))
                        except IOError:
                            isThereListener = False
                            listenerConn.close()
                            del frames[:]
                            
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
    print 'waiting for speaker'
    speakerSocket.listen(1)
    conn, addr = speakerSocket.accept()
    print 'get speaker at', addr, isThereListener
    count = 0;
    while 1:
        try:
            data = conn.recv(CHUNK*CHANNELS*2)
            if not data: break
            if isThereListener:
                frames.append(data)
        except IOError:
            del frames[:]
            break
    conn.close()

lt.stop()
speakerSocket.close()
    
