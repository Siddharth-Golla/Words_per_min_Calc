import curses
import time
from curses import wrapper
import random


def start_screen(stdscr):

    # Starting Welcome Screen

    stdscr.clear()
    stdscr.addstr("Welcome to Speed Typing Test!", curses.color_pair(2))
    stdscr.addstr("\n\nThis is a simple word per minute calculator where you will be given a random line and WPM is calculated as you type in", curses.color_pair(3))
    stdscr.addstr("\n\nPress any key to start typing..", curses.color_pair(2))
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):

    # Applying green color to correct character and red to incorrect character

    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"Words per minute : {wpm}")

    for i, char in enumerate(current):
        correct_character = target[i]
        color = curses.color_pair(1)
        if char != correct_character:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def load_text():

    # Opening text.txt and returning random line
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    words_per_min = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        # Calculating words per minute
        time_elapsed = max(time.time() - start_time, 1)
        characters_per_min = len(current_text) / (time_elapsed / 60)

        # Assuming average characters in a word are 5
        words_per_min = round(characters_per_min / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, words_per_min)
        stdscr.refresh()

        # After user enters complete correct text
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        # Exiting on Esc key press
        if ord(key) == 27:
            break

        # Checking whether BACKSPACE is pressed
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()

        # Adding characters to current_text till len(current_text) = len(target_text)
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    # Creating color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

        stdscr.addstr(
            2, 0, "You completed the test! Press any key to play again or Esc to Exit..")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
