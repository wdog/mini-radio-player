#!/bin/env python3

import sys
import os
import time
import logging
from station import Station
from player import Player

import curses
import time

class Radio():

    top = 0
    max_lines = 0
    play_station = None

    """description"""
    def __init__(self):
        self.init_curses()
        # station manager
        self.sm= Station()
        self.player = Player()
        

    def init_curses(self):
        self.screen = curses.initscr()
        #init curses and curses input
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0) 
        self.screen.keypad(1)

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_GREEN)

        # defin max row 
        h,w = self.screen.getmaxyx()

        self.max_lines = h//2
        self.padchars = w - 20
    def draw(self):

        self.current_station = 0
        self.draw_menu()

        while True:
            key = self.screen.getch()
            self.screen.clear()
            # quit key
            down_keys = [curses.KEY_DOWN, ord('j')]
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [ord('q')]
            play_keys = [curses.KEY_ENTER, ord('p'), 10, 13 ]
            info_keys = [ord('i')]


            if key in exit_keys:
                logging.warn('bye')
                break

            if key in down_keys and self.current_station < len(self.sm.stations) - 1:
                self.current_station += 1

            if key in up_keys  and self.current_station > 0 :
                self.current_station -= 1
    
            if key in play_keys:
                self.play_station = self.sm.stations[self.current_station]
                self.player.load_station(self.play_station)
                self.player.play()

            if key in info_keys:
                m = self.player.get_info()
                #logging.info(help(m))
                logging.info(m.get_duration())

            self.draw_menu()
        

    def draw_menu(self):
        
        self.screen.border()
        h ,w = self.screen.getmaxyx()
        self.screen.addstr(0 ,w//2, "~ MINI RADIO PLAYER ~", curses.color_pair(3) )

        if self.current_station + 1 == self.top  and self.current_station >= 0  :
            self.top -= 1

        if self.current_station == self.top + self.max_lines :
            self.top += 1

        for idx, item in enumerate(self.sm.stations[self.top:self.top + self.max_lines]):
            row_idx= idx + self.top
            # set color 
            color =  curses.color_pair(3) if row_idx == self.current_station else curses.color_pair(1)
            self.screen.addstr(idx + 2, 5, '{}. {}'.format( str(row_idx+1).rjust(4,' ') ,item['name'].ljust(self.padchars,'.')), color)

        # Render status bar
        statusbarstr = "Press 'q' to exit | STATUS BAR | {}".format(self.play_station['name'] if self.play_station else '')
        self.screen.attron(curses.color_pair(3))
        self.screen.addstr(h-2, 1, statusbarstr)
        self.screen.addstr(h-2, len(statusbarstr) + 1, " " * (w - len(statusbarstr) - 1))
        self.screen.attroff(curses.color_pair(3))



        self.screen.refresh()

    def run(self):
            """Continue running the TUI until get interrupted"""
            try:
                self.draw()
            except KeyboardInterrupt:
                pass
            finally:
                curses.endwin()
        

def main():
    r= Radio()
    r.run()

if __name__ == '__main__':
    logging.basicConfig(filename='radio.log',level=logging.INFO)
    main() 
