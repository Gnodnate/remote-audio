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

class msgReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
    def run(self):
        while not self.thread_stop:
            global listenerAddr
            try:
                msg, address = msgSocket.recvfrom(1024)
            except socket.timeout:
                continue
            print msg, address
            listenerAddr = address
            if msg == 'start transfer':
                isListenerOnLine = True
                msgSocket.sendto(msg, listenerAddr)
            if msg == 'quit transfer':
                isListenerOnLine = False

    def stop(self):
        self.thread_stop = True

msgThread = msgReceiver()
msgThread.setDaemon(True)
msgThread.start()

dataSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
dataSocket.bind(('', 18965))

print 'wait speaker at 18965'
while True:
    try:
        data, addr = dataSocket.recvfrom(65536)
    except socket.timeout:
        continue
    print "Get speaker",addr
    if isListenerOnLine:
        dataSocket.sendto(data, listenerAddr)
    else:
        time.sleep(1)

msgThread.stop()
msgSocket.close()
dataSocket.close()
    
