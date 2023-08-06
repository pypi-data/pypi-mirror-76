# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:09:28 2020

@author: marku
"""
import serial
from .BaseCom import BaseCom
import time

class SerialCom(BaseCom):
    def __init__(self, addr, conTimeout=1, ioTimeout=0.5, trace=False, traceCB=None):
        self.comPort = addr[0]
        self.conTimeout = conTimeout
        self.ioTimeout = ioTimeout
        BaseCom.__init__(self, trace, traceCB)
                
    def _write(self, data):
        self.ser.write(data)
        
    def _read(self, nbytes):
        d = self.ser.read(nbytes)
        return d
   
    def _connect(self):
        self.ser = serial.Serial(port=self.comPort, baudrate=115200, timeout=self.conTimeout)
        self.ser.timeout = self.ioTimeout
        data = b""
        lastRcv = time.time()
        while True:
            data = self.readLine()
            if data.find(b"Committing updates in NVS ... Done") != -1:
                break
            if data != b"":
                lastRcv = time.time()
            if time.time() - lastRcv > 10:
                break
        
    def _clear(self):
        nbytes = self.ser.inWaiting()
        self.ser.read(nbytes)
        
    def _disconnect(self):
        self.ser.close()