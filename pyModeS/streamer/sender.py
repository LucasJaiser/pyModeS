#!/usr/bin/env python
import json
import logging
import time
import traceback
from getmac import get_mac_address
from pyModeS.extra.gps import Gps

import requests


class Sender(object):
    def __init__(self, url, polling_interval=1):
        super(Sender, self).__init__()
        self.server_url = url
        self.polling_interval = polling_interval
        self.acs = {}

    def send_data(self, exception_queue, current_position):
        if len(self.acs) == 0:
            return

        headers = {'Content-Type': 'application/json'}
        for icao, ac in self.acs.items():
            if not ac.get("lat") or not ac.get("lon"):
                continue

            ac_data = {
                "icao": icao,
                "callsign": ac.get("call", "") or '',
                "x": ac.get("lon"),
                "y": ac.get("lat"),
                "altitude": ac.get("alt", 0) or 0,
                "groundspeed": ac.get("gs", 0) or 0,
                "trueairspeed": ac.get("tas", 0) or 0,
                "indicatedairspeed": ac.get("ias", 0) or 0,
                "trackangle": ac.get("trk", 0) or 0,
                "magneticheading": ac.get("hdg", 0) or 0,
                "station": {
                    "mac": get_mac_address().replace(':', '').upper(),
                    "x": current_position[0],
                    "y": current_position[1]
                }
            }

            try:
                json_data = json.dumps(ac_data)
            except Exception as e:
                logging.error(e)
                trace_exc = traceback.format_exc()
                exception_queue.put(trace_exc)
                time.sleep(0.1)
            
            try:
                response = requests.post(self.server_url, headers=headers, data=json_data)
                if response.status_code > 400:
                    logging.error(response.content)
            except requests.exceptions.ConnectionError as con_err:
                logging.error(con_err)
                trace_exc = traceback.format_exc()
                exception_queue.put(trace_exc)
                time.sleep(0.1)
                

    def run(self, ac_pipe_out, exception_queue):
        gps = Gps()
        gps.start()
        
        local_buffer = []
        while True:
            try:
                while ac_pipe_out.poll():
                    acs = ac_pipe_out.recv()
                    local_buffer.append(acs)

                for msg in local_buffer:
                    self.acs = msg

                local_buffer.clear()
                self.send_data(exception_queue, gps.get_current_position())

            except Exception as e:
                trace_exc = traceback.format_exc()
                exception_queue.put(trace_exc)
                time.sleep(0.1)
                raise e

            time.sleep(self.polling_interval)
