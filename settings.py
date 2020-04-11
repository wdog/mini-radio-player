import curses

class CursesSettings():
    
    def __init__(self,radio):
       
        self.screen = radio.screen
        self.screen.keypad(1)  # enable keyboard use
        # defin max row
        h, w = self.screen.getmaxyx()
        self.max_lines = h - 6
        self.padchars = w - 20


        # init curses and curses input

        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)  # hide cursor
       

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)

        # border color
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

        
        
    
