#!/usr/bin/env python3

import sys
import os
import time
import logging
from station import Station
from player import Player
from settings import CursesSettings

import curses
import time

"""Radio"""


class Radio():

    top = 0
    info_station = []
    current_station = 0

    """ Init """
    def __init__(self):
        self.screen = curses.initscr()    
        # settings     
        self.settings = CursesSettings(self)   
        # station manager
        self.sm = Station()
        self.play_station = self.sm.stations[self.current_station]
        # player 
        self.player = Player()
        
    def spinning_cursor(self):
        while True:
            for cursor in '⠁⠂⠄⡀⢀⠠⠐⠈':
                yield cursor


    """ Draw Menu Main Function """
    def draw(self):
        self.spinner = self.spinning_cursor()
        while True:
            self.draw_menu()
            self._check_events()
    
    """ Draw Menu """
    def draw_menu(self):
        self.screen.attron(curses.color_pair(4))
        self.screen.border(0)
        self.screen.attroff(curses.color_pair(4))

        h, w = self.screen.getmaxyx()
        title = "~ MINI RADIO PLAYER ~"
        self.screen.addstr(0, w//2 - len(title)//2,
                           title, curses.color_pair(3))

        if self.current_station + 1 == self.top and self.current_station >= 0:
            self.top -= 1

        if self.current_station == self.top + self.settings.max_lines:
            self.top += 1

        for idx, item in enumerate(self.sm.stations[self.top:self.top + self.settings.max_lines]):
            row_idx = idx + self.top
            # set color
            color = curses.color_pair(
                3) if row_idx == self.current_station else curses.color_pair(1)
            self.screen.addstr(idx + 2, 5, '{}. {}'.format(str(row_idx+1).rjust(
                4, ' '), item['name'].ljust(self.settings.padchars, '.')), color)

        # Render status bar station info
        statusbarstr = " - ".join(self.info_station[:1])
        statusbarstr = statusbarstr[0:w-10]
        self.screen.attron(curses.color_pair(3))
        self.screen.addstr(h-4, 1, statusbarstr)
        self.screen.addstr(h-4, len(statusbarstr) + 1, " " * (w - len(statusbarstr) - 2))

        self.screen.addstr(h-4, w-8, "[" + next(self.spinner) + "]" )
        self.screen.attroff(curses.color_pair(3))

        
        # Render status bar station info
        if len(self.info_station) > 2:
            statusbarstr = self.info_station[2]
            statusbarstr = statusbarstr[0:w-10]
            self.screen.attron(curses.color_pair(2))
            self.screen.addstr(h-3, 1, statusbarstr)
            self.screen.addstr(h-3, len(statusbarstr) + 1,
                            " " * (w - len(statusbarstr) - 2))
            self.screen.attroff(curses.color_pair(2))



        # Render status bar
        statusbarstr = "Press (q) exit (i) info, (p) play,(t|spacebar) toggle (1-9) shortcuts (c) credits"
        statusbarstr = statusbarstr[0:w-10]
        self.screen.attron(curses.color_pair(3))
        self.screen.addstr(h-2, 1, statusbarstr)
        self.screen.addstr(h-2, len(statusbarstr) + 1,
                           " " * (w - len(statusbarstr) - 2))
        self.screen.attroff(curses.color_pair(3))

    """ Show Credits for 3 seconds """
    def show_credits(self):
        h, w = self.screen.getmaxyx()
        self.screen.erase()
        title = "CODED WITH LOVE"
        self.screen.addstr(h//2, (w - len(title))//2, title)
        subtitle = "wdog <wdog666@gmail.com>"
        self.screen.addstr(h//2+2, (w - len(subtitle))//2, subtitle)
        self.screen.refresh()
        time.sleep(3)

    """Continue running the TUI until get interrupted"""   
    def run(self):
        try:
            self.draw()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def setPlay(self):
        """setPlay"""
        self.play_station = self.sm.stations[self.current_station]
        self.player.load_station(self.play_station)
        self.player.play()
        self.info_station = self.player.get_info()
        

    """ Check Events """
    def _check_events(self):
        key = self.screen.getch()
            
        # quit key
        down_keys = [curses.KEY_DOWN, ord('j')]
        up_keys = [curses.KEY_UP, ord('k')]
        exit_keys = [ord('q'),ord('Q')]
        play_keys = [curses.KEY_ENTER, ord('p'),ord('P'), 10, 13]
        info_keys = [ord('i')]
        play_toggle = [ord('t'),ord(' ')]
        info_credits = [ord('c')]



        # quit
        if key in exit_keys:
            sys.exit()

        # key down
        if key in down_keys and self.current_station < len(self.sm.stations) - 1:
            self.current_station += 1

        # key up
        if key in up_keys and self.current_station > 0:
            self.current_station -= 1

        # key play
        if key in play_keys:
            self.setPlay()

        # key get station info
        if key in info_keys:
            self.info_station = self.player.get_info()

        # key toggle play
        if key in play_toggle:
            self.player.toggle()
            if not self.player.is_playing:
                self.info_station = ['STOPPED','','']
            else:
                self.info_station = self.player.get_info()
        
        # key for show credits
        if key in info_credits:
            self.show_credits()

        filter_keys = [str(i) for i in range(1,len(self.sm.stations))]
        if chr(key) in filter_keys:
            v = int(chr(key))-1
            self.current_station = v
            self.setPlay()

    
""" MAIN """
def main():
    r = Radio()
    r.run()

if __name__ == '__main__':
    logging.basicConfig(filename='radio.log', level=logging.DEBUG, format='  %(asctime)s - %(levelname)s - %(message)s')
    logging.debug('start radio')
    main()
