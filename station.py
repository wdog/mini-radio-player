import logging
import json

class Station:
    """description"""
    stations =[]

    def __init__(self):
        self.load_stations_list()

    def load_stations_list(self):
        """Load radio station list"""
        with open('radio.json') as f:
            self.stations = json.load(f)

        
        
