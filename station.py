import logging
import json


class Station:
    """STATION CLASS - MANAGES RADIO LIST"""
    stations = []

    def __init__(self):
        self.load_stations_list()

    def load_stations_list(self):
        """Load radio station list"""
        with open('radio.json') as f:
            self.stations = json.load(f)

    def change_order(self, src, dst):
        """ rewrite stations file with different order """
        origSrc = self.stations[src]
        self.stations[src] = self.stations[dst]
        self.stations[dst] = origSrc
        try:  
            with open('radio.json','w') as f:
                json.dump(self.stations,f)
        except Exception as e:
            logging.warn(e)
