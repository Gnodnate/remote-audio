#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
import pyaudio
import threading

frames= []

class udpStream(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
    def run(self):
        server_address = ('162.217.*.*', 18965)
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect(server_address)
        while not self.thread_stop:
            if len(frames) > 0:
                try:
                    tcp.sendall(frames.pop(0))
                except:
                    break
                    
        tcp.close()
        
    def stop(self):
        self.thread_stop = True

udpTread = udpStream()
udpTread.setDaemon(True)
udpTread.start()

CHUNK = 1024
CHANNELS = 1
RATE = 44100
FORMAT = pyaudio.paInt16


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while True:
    data = stream.read(CHUNK)
    frames.append(data)
    
stream.stop_stream()
stream.close()
p.terminate()
