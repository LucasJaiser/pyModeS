#!/usr/bin/env python

import serial


def convert_to_degrees(raw_value):
    decimal_value = raw_value / 100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - degrees) / 0.6
    position = degrees + mm_mmmm
    return '%.4f' % position


class Gps(object):
    def __init__(self, serial_port='/dev/ttyS0'):
        super(Gps, self).__init__()
        self.serial_port = serial.Serial(serial_port)  # mini-UART (/dev/ttyS0) interface on RPi 4
        self.gpgga_buffer = 0
        self.nmea_buffer = 0

    def get_current_position(self):
        try:
            while True:
                data = str(self.serial_port.readline())  # read NMEA string
                if data.find('$GPGGA,') > 0:
                    self.gpgga_buffer = data.split('$GPGGA,', 1)[1]  # store data coming after “$GPGGA,” string
                    self.nmea_buffer = self.gpgga_buffer.split(', ')
                    nmea_latitude = self.nmea_buffer[1]  # extract latitude from GPGGA string
                    nmea_longitude = self.nmea_buffer[3]  # extract longitude from GPGGA string
                    lat = convert_to_degrees(float(nmea_latitude))
                    lon = convert_to_degrees(float(nmea_longitude))
                    print(f'Lat: {lat} Long: {lon}', '\n')
                    return lat, lon
        except Exception as e:
            return -1, -1



