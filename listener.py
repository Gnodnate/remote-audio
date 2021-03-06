#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import sys
import pyaudio

serverAddr = ('162.217.249.194', 18964)
cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliSocket.connect(serverAddr)
tryCount = 0
while 1:
    cliSocket.send('start transfer')
    try:
        msg = cliSocket.recv(512)
        print msg
        if msg == 'start transfer':
            break
    except socket.timeout:
        if tryCount < 5:
            continue
    if tryCount >= 5:
        break
    tryCount +=1
    print tryCount

if tryCount >= 5:
    print "Can't connect to server:",serverAddr
    exit()


CHUNK = 1024
CHANNELS = 1
RATE = 44100
FORMAT = pyaudio.paInt16
pa = pyaudio.PyAudio() 
stream = pa.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      output=True)
tryCount = 0
while 1:
    try:
        data = cliSocket.recv(CHUNK*CHANNELS*2)
        print 'get len',len(data)
        if not data:
            break
    except socket.timeout:
        if tryCount > 5:
            print "No one is there"
            break
        else:
            tryCount += 1
            continue
    stream.write(data)

cliSocket.send('quit transfer')
cliSocket.close()
stream.stop_stream()
stream.close()
pa.terminate()
        
