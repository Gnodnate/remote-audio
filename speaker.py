#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from datetime import datetime
import socket
import pyaudio
import threading

frames= []

class udpStream(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
    def run(self):
        server_address = ('162.217.249.194', 18965)
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not self.thread_stop:
            if len(frames) > 0:
                udp.sendto(frames.pop(0), server_address)
                
        udp.close()
        
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
save_count = 0 
save_buffer = [] 
large_sample_count = 0

while True:
    data = stream.read(CHUNK)
    frames.append(data)
    
stream.stop_stream()
stream.close()
p.terminate()
