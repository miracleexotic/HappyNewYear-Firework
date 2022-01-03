import curses
from curses import wrapper
import time
import random
import threading

TIME = 0.1
LINES = 100
COLS = 100
BORDER = 5
SCREEN = 30
TAIL_FIREWORK = 3

def main(stdscr):

    stdscr.clear()

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

    myColour = [
        curses.COLOR_BLUE,
        curses.COLOR_MAGENTA,
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_YELLOW,
    ]

    myColour_lenght = len(myColour)
    for i in range(myColour_lenght):
        curses.init_pair(i+5, myColour[i], -1)
    
    pad = curses.newpad(LINES+1, COLS+1)
    stdscr.refresh()

    lstRol = []
    for y in range(0, LINES-TAIL_FIREWORK):
        head = []
        for x in range(0, COLS):
            if x == random.randint(BORDER, COLS-BORDER) and SCREEN < y < LINES-SCREEN-TAIL_FIREWORK:
                head.append(x)
                pad.addstr(0+y,x, "^", curses.color_pair(1))
                pad.addstr(1+y,x, "*", curses.color_pair(2))
                pad.addstr(2+y,x, "!", curses.color_pair(3))
                pad.addstr(3+y,x, ".", curses.color_pair(4))
                continue
        lstRol.append(head)
    
    pad.addstr(LINES,0, "="*COLS)

    def explosion(y, x):
        for i in range(4):
            colour = curses.color_pair(random.randint(5, 5+myColour_lenght-1))
            if i == 0:
                pad.addstr(y+i-1,x, "     |     ", colour)
                pad.addstr(y+i,x,   "   - 0 -   ", colour)
                pad.addstr(y+i+1,x, "     |     ", colour)
                pad.addstr(y+i-2,x, "           ", colour)
            elif i == 1:
                pad.addstr(y+i-1,x, "   \ . /   ", colour)
                pad.addstr(y+i,x,   "  -- O --  ", colour)
                pad.addstr(y+i+1,x, "   / | \   ", colour)
                pad.addstr(y+i-2,x, "           ", colour)
            elif i == 2:
                pad.addstr(y+i-1,x, " . -. .- . ", colour)
                pad.addstr(y+i,x,   ". -  *  - .", colour)
                pad.addstr(y+i+1,x, "   . | .   ", colour)
                pad.addstr(y+i-2,x, "           ", colour)
            elif i == 3:
                pad.addstr(y+i-1,x, "           ", colour)
                pad.addstr(y+i,x,   ".    .    .", colour)
                pad.addstr(y+i+1,x, "  .     .  ", colour)
                pad.addstr(y+i-2,x, "           ", colour)

            time.sleep(TIME)

        for i in range(4):
            pad.addstr(y+2+i,x, "           ")

    def position(pos):
        exploPos = i+pos
        head = lstRol[exploPos]
        pad.addstr(i+3,0, " "*COLS)
        if len(head) > 0:
            for x in head:
                thr = threading.Thread(target=explosion, args=(exploPos, x))
                thr.start()
                thr.join()

    def banner(line):
        if line < 60:
            return
        row = ["                                                                             ",
               " _                                                                           ",
               "| |__   __ _ _ __  _ __  _   _   _ __   _____      __  _   _  ___  __ _ _ __ ",
               "| '_ \ / _` | '_ \| '_ \| | | | | '_ \ / _ \ \ /\ / / | | | |/ _ \/ _` | '__|",
               "| | | | (_| | |_) | |_) | |_| | | | | |  __/\ V  V /  | |_| |  __/ (_| | |   ",
               "|_| |_|\__,_| .__/| .__/ \__, | |_| |_|\___| \_/\_/    \__, |\___|\__,_|_|   ",
               "            |_|   |_|    |___/                         |___/                 ",
               "                                                                             ",                                      
               "                    .-----.   .----.   .-----.  .-----.                      ",
               "                   / ,-.   \ /  ..  \ / ,-.   \/ ,-.   \                     ",
               "                   '-'  |  |.  /  \  .'-'  |  |'-'  |  |                     ",
               "                      .'  / |  |  '  |   .'  /    .'  /                      ",
               "                    .'  /__ '  \  /  ' .'  /__  .'  /__                      ",
               "                   |       | \  `'  / |       ||       |                     ",
               "                   `-------'  `---''  `-------'`-------'                     "
               ]

        row_lenght = len(row[0])
        for i in range(len(row)):
            pad.addstr(line-25+i, (COLS-row_lenght)//2, row[i])


    for i in range(0, LINES-SCREEN+1):
        thr_banner = threading.Thread(target=banner, args=(i+SCREEN,))
        thr_banner.start()
        thr_fix = threading.Thread(target=position, args=(5,))
        thr_fix.start()
        thr_random = threading.Thread(target=position, args=(random.randint(5,15),))
        thr_random.start()

        pad.refresh( i,0, 0,0, SCREEN,COLS)
        time.sleep(TIME)

    for i in range(0, LINES-10, 16):
        pad.addstr(LINES-3,  0+i, "  o        ")
        pad.addstr(LINES-2,  0+i, " /|\\      ")
        pad.addstr(LINES-1,  0+i, " / \\      ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  1+i, " \o/       ")
        pad.addstr(LINES-2,  1+i, "  |        ")
        pad.addstr(LINES-1,  1+i, " / \\      ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  2+i, " _ o       ")
        pad.addstr(LINES-2,  2+i, "  /\\      ")
        pad.addstr(LINES-1,  2+i, " | \\      ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  3+i, "           ")
        pad.addstr(LINES-2,  3+i, "  __\o     ")
        pad.addstr(LINES-1,  3+i, " /)  |     ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  4+i, " __|       ")
        pad.addstr(LINES-2,  4+i, "   \o      ")
        pad.addstr(LINES-1,  4+i, "   ( \\    ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  5+i, "   \ /     ")
        pad.addstr(LINES-2,  5+i, "    |      ")
        pad.addstr(LINES-1,  5+i, "   /o\\    ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  6+i, "     |__   ")
        pad.addstr(LINES-2,  6+i, "    o/     ")
        pad.addstr(LINES-1,  6+i, "   / )     ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  7+i, "           ")
        pad.addstr(LINES-2,  7+i, "    o/__   ")
        pad.addstr(LINES-1,  7+i, "    |   (\\")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  8+i, "       o _ ")
        pad.addstr(LINES-2,  8+i, "       /\  ")
        pad.addstr(LINES-1,  8+i, "       / | ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)
        pad.addstr(LINES-3,  9+i, "        o  ")
        pad.addstr(LINES-2,  9+i, "       /|\ ")
        pad.addstr(LINES-1,  9+i, "       / \ ")
        pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
        time.sleep(0.2)

    pad.addstr(LINES-3, COLS-10, "           ")
    pad.addstr(LINES-2, COLS-10, "           ")
    pad.addstr(LINES-1, COLS-10, "           ")
    pad.refresh( LINES-SCREEN,0, 0,0, SCREEN,COLS)
    time.sleep(0.2)

    stdscr.getkey()

wrapper(main)

