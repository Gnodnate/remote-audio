#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
from datetime import datetime
import socket
import pyaudio

CHUNK = 256
WIDTH = 2
CHANNELS = 1
RATE = 44100

# 开启声音输入
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
save_count = 0 
save_buffer = [] 
large_sample_count = 0

# UDP socket
speakerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('162.217.249.194', 18965)
#while True: 
    # 读入NUM_SAMPLES个取样
data = stream.read(CHUNK)
stream.write(data, CHUNK)
print 'send data',speakerSocket.sendto(data, server_address)
    
stream.stop_stream()
stream.close()
p.terminate()
