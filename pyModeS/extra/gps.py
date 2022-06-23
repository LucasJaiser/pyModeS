#!/usr/bin/env python

import serial
import threading
import time
import re


def convert_to_degrees(raw_value):
    decimal_value = raw_value / 100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - degrees) / 0.6
    position = degrees + mm_mmmm
    return '%.4f' % position


class Gps(threading.Thread):
    def __init__(self, serial_port='/dev/serial0'):
        threading.Thread.__init__(self)
        self.serial_port = serial.Serial(serial_port, baudrate=9600, timeout=1)  # mini-UART (/dev/ttyS0) interface on RPi 4
        self.current_position = (-1, -1)
        
    def get_current_position(self):
       return self.current_position
    
    def run(self):
       try:
            while True:
                data = str(self.serial_port.readline())  # read NMEA string for serial interface
                if not data:
                    continue
                
                nmea_msg_buffer = data.split(',')
                nmea_sentence = nmea_msg_buffer[0]
                
                # GGA – Global positioning system (GPS) fix data
                # $GNGGA,185833.80,4808.7402397,N,01133.9325039,E,5,15,1.1,470.50,M,45.65,M,,*75
                # lat [2] lon [4]
                if re.search('\$G[P|N]GGA', nmea_sentence, re.IGNORECASE):# GGA: $G[P/N]GGA
                    if not nmea_msg_buffer[2] or not nmea_msg_buffer[4]:
                        continue
                    
                    nmea_latitude = float(nmea_msg_buffer[2])  # extract latitude from GGA string
                    nmea_longitude = float(nmea_msg_buffer[4])  # extract longitude from GGA string
                    self.current_value = (convert_to_degrees(nmea_latitude), convert_to_degrees(nmea_longitude))

                
                # RMC – Recommended minimum specific GNSS data
                # $GNRMC,185823.40,A,4808.7402374,N,01133.9324760,E,0.00,112.64,130117,3.00,E,A*14
                # lat [3] lon [5]
                elif re.search('\$G[P|N]RMC', nmea_sentence, re.IGNORECASE): # RMC: $G[P/N]RMC
                    if not nmea_msg_buffer[3] or not nmea_msg_buffer[5]:
                        continue
                    
                    nmea_latitude = float(nmea_msg_buffer[3])  # extract latitude from RMC string
                    nmea_longitude = float(nmea_msg_buffer[5])  # extract longitude from RMC string
                    self.current_value = (convert_to_degrees(nmea_latitude), convert_to_degrees(nmea_longitude))
       except StopIteration:
            pass