#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import sys
import pyaudio

serverAddr = ('162.217.249.194', 18964)
#serverAddr = ('45.62.127.222', 18964)
cliSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliSocket.settimeout(5)
tryCount = 0
while 1:
    cliSocket.sendto('start transfer', serverAddr)
    try:
        msg, addr = cliSocket.recvfrom(2048)
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
#    exit()

# 开启声音
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
        data, addr = cliSocket.recvfrom(CHUNK*CHANNELS*2)
    except socket.timeout:
        if tryCount > 5:
            print "No one is there"
            break
        else:
            tryCount += 1
            continue
    stream.write(data)

cliSocket.sendto('quit transfer', serverAddr)
cliSocket.close()
stream.stop_stream()
stream.close()
pa.terminate()
        
