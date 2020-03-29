#!/usr/bin/env python3

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
    info_station = []

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
        curses.curs_set(0) # hide cursor 
        self.screen.keypad(1) #enable keyboard use

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)

        #border color
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

        # defin max row 
        h,w = self.screen.getmaxyx()

        self.max_lines = h - 6
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
            play_toggle = [ord('t')]
            info_credits = [ord('c')]

            # quit
            if key in exit_keys:
                logging.warn('bye')
                break

            # key down
            if key in down_keys and self.current_station < len(self.sm.stations) - 1:
                self.current_station += 1

            # key up
            if key in up_keys  and self.current_station > 0 :
                self.current_station -= 1

            # key play
            if key in play_keys:
                self.play_station = self.sm.stations[self.current_station]
                self.player.load_station(self.play_station)
                self.player.play()
                self.info_station = self.player.get_info()

            # key get station info
            if key in info_keys:
                self.info_station = self.player.get_info()

            # key toggle play 
            if key in play_toggle:
                self.player.toggle()
                if not self.player.is_playing:
                    self.info_station.clear()
                    self.info_station.append('STOPPED')
                else:
                    self.info_station = self.player.get_info()



            if key in info_credits:
                self.show_credits()

            self.draw_menu()
        

    def draw_menu(self):
        
        self.screen.attron(curses.color_pair(4))
        self.screen.border(0)
        self.screen.attroff(curses.color_pair(4))

        h ,w = self.screen.getmaxyx()
        title = "~ MINI RADIO PLAYER ~"
        self.screen.addstr(0 ,w//2 - len(title)//2, title , curses.color_pair(3) )

        if self.current_station + 1 == self.top  and self.current_station >= 0  :
            self.top -= 1

        if self.current_station == self.top + self.max_lines :
            self.top += 1

        for idx, item in enumerate(self.sm.stations[self.top:self.top + self.max_lines]):
            row_idx= idx + self.top
            # set color 
            color =  curses.color_pair(3) if row_idx == self.current_station else curses.color_pair(1)
            self.screen.addstr(idx + 2, 5, '{}. {}'.format( str(row_idx+1).rjust(4,' ') ,item['name'].ljust(self.padchars,'.')), color)

        # Render status bar station info
        statusbarstr = " - ".join(self.info_station)
        statusbarstr = statusbarstr[0:w-10] 
        self.screen.attron(curses.color_pair(2))
        self.screen.addstr(h-3, 1, statusbarstr)
        self.screen.addstr(h-3, len(statusbarstr) + 1, " " * (w - len(statusbarstr) - 2))
        self.screen.attroff(curses.color_pair(2))

        # Render status bar
        statusbarstr = "Press 'q' to exit, 'i' info, 'p' play,'t' toggle, 'c' credits| {}".format(self.play_station['name'] if self.play_station else '')
        statusbarstr = statusbarstr[0:w-10] 
        self.screen.attron(curses.color_pair(3))
        self.screen.addstr(h-2, 1, statusbarstr)
        self.screen.addstr(h-2, len(statusbarstr) + 1, " " * (w - len(statusbarstr) - 2))
        self.screen.attroff(curses.color_pair(3))

    def show_credits(self):
        h ,w = self.screen.getmaxyx()
        self.screen.erase()
        title = "CODED WITH LOVE"
        self.screen.addstr(h//2, (w - len(title))//2, title)
        subtitle = "wdog <wdog666@gmail.com>"
        self.screen.addstr(h//2+2, (w - len(subtitle))//2, subtitle) 
        self.screen.refresh()
        time.sleep(3)

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
