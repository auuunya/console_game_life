#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/07/08 11:37:30
@Desc    :   None
'''

# here put the import lib
import random, os, time, argparse, curses
from functools import reduce


ALIVE = 1
DIED = 0
ROW_CHARS = "-"
LINE_CHARS = "|"
MAX_TIME = 5.0

def row_state(width, ranint=False):
    if ranint:
        return [ALIVE if random.random() >= 0.5 else DIED for _ in range(width)]
    return [DIED for _ in range(width)]

def _get_states(height, rows):
    return [rows for _ in range(height)]

def died_state(width, height):
    states = [[DIED for _ in range(width)] for _ in range(height)]
    return states

def random_state(width, height):
    states = [row_state(width, ranint=True) for _ in range(height)]
    return states

RESET_COLOR = "\033[0m"
ALIVE_COLOR = "\033[92m"  # Green for alive cells
DIED_COLOR = "\033[90m"   # Grey for dead cells
RED_COLOR = "\033[91m"
def render(states):
  clear()
  alive_count = 0
  top_border = "+" + "-" * len(states[0]) + "+"
  print(top_border)
  for row in states:
      var_char = "|"
      for item in row:
          if item:
              alive_count += 1
              var_char += ALIVE_COLOR + "#" + RESET_COLOR
          else:
              var_char += DIED_COLOR + "." + RESET_COLOR
      var_char += "|"
      print(var_char)
  bottom_border = "+" + "-" * len(states[0]) + "+"
  print(bottom_border)
  print(f"{RED_COLOR}alive count: {alive_count}{RESET_COLOR}\n")

def render_str(states):
  alive_count = 0
  render_content = ""
  top_border = "+" + "-" * len(states[0]) + "+\n"
  render_content += render_content
  for row in states:
      var_char = "|"
      for item in row:
          if item:
              alive_count += 1
              var_char += ALIVE_COLOR + "#" + RESET_COLOR
          else:
              var_char += DIED_COLOR + "." + RESET_COLOR
      var_char += "|"
      render_content = render_content + var_char + "\n"
  bottom_border = "+" + "-" * len(states[0]) + "+\n"
  render_content += bottom_border
  return render_content, alive_count

def next_board_state(init_state):
    lines = len(init_state)
    rows = len(init_state[0])
    new_state = died_state(rows, lines)
    for line in range(lines):
        for row in range(rows):
            total_list = around_martix(line, row, rows, lines)
            total = sum(init_state[i[0]][i[1]] for i in total_list)
            if total == 3:
                new_state[line][row] = ALIVE
            elif total == 2:
                new_state[line][row] = init_state[line][row]
            else:
                new_state[line][row] = DIED
    return new_state


def around_martix(y, x, rows, lines):
    total_list = []
    max_y = max(y if y + 1 >= lines else y + 1, y)
    min_y = min(0 if y - 1 < 0 else y - 1, y)
    max_x = max(x if x + 1 >= rows else x + 1, x)
    min_x = min(0 if x - 1 < 0 else x - 1, x)
    for j in range(min_y, max_y + 1):
        for i in range(min_x, max_x + 1):
            if i == x and j == y:
                continue
            total_list.append([j, i])
    return total_list


def load_board_state(file):
    with open(file) as f:
        lines = f.readlines()
        init_states = []
        for line in lines:
            init_states.append([int(i) for i in list(line.strip())])
        return init_states

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_arguments():
    parser = argparse.ArgumentParser(
        prog="Console Game Life",
        description="A console implementation of Conway's Game of Life.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path to a file containing the initial state as lines of '0' and '1'."
    )
    parser.add_argument(
        "-r",
        "--random",
        nargs=2,
        metavar=('rows', 'cols'),
        type=int,
        help="Generate a random 2D array with specified dimensions (rows and cols)."
    )
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        default=0.5,
        help="Time interval between each iteration in seconds (default is 0.5 second)."
    )
    args = parser.parse_args()
    if args.file and args.random:
        parser.error("Arguments -f/--file and -r/--random cannot be used together.")
    if args.time > MAX_TIME:
        parser.error(f"The time interval cannot exceed {MAX_TIME} seconds.")
    if args.time < 0:
        args.time = 0.5
    return args


help_messages = [
    "Help:",
    "Press 'Q' or 'q' to quit."
]
def draw_render(win, states):
    alive_count = 0
    moveY = 0
    maxHeight, maxWidth = win.getmaxyx()
    cols = len(states)
    rows = len(states[0])
    if rows + 2 > maxWidth:
        states = random_state(maxWidth, cols)
    if cols + 4 > maxHeight:
        states = random_state(rows, maxHeight)

    for help_message in help_messages:
        win.addstr(moveY, 0, help_message)
        moveY += 1
    moveY = moveY + 1
    top_border = "+" + "-" * len(states[0]) + "+"
    win.attron(curses.color_pair(1))
    win.addstr(moveY, 0, top_border)
    win.attroff(curses.color_pair(1))
    for row in states:
        var_char = "|"
        moveX = 1
        moveY += 1
        win.attron(curses.color_pair(1))
        win.addstr(moveY, 0, "|")
        win.attroff(curses.color_pair(1))
        for item in row:
            moveX += 1
            if item:
                alive_count += 1
                var_char += "#" 
                win.attron(curses.color_pair(2))
                win.addstr(moveY, moveX, "#")
                win.attroff(curses.color_pair(2))
            else:
                var_char += "."
                win.attron(curses.color_pair(1))
                win.addstr(moveY, moveX, ".")
                win.attroff(curses.color_pair(1))
        var_char += "|"
        
        win.attron(curses.color_pair(1))
        win.addstr(moveY, len(row) + 1, "|")
        win.attroff(curses.color_pair(1))
        # win.addstr(moveY, 0, var_char)
    bottom_border = "+" + "-" * len(init_states[0]) + "+"
    win.attron(curses.color_pair(1))
    win.addstr(moveY, 0, bottom_border)
    win.attroff(curses.color_pair(1))
    moveY += 1
    win.addstr(moveY,0, f"Alive Count: {alive_count}")
    win.refresh()

def draw(init_states):
    stdscr = curses.initscr()    
    curses.curs_set(0)
    stdscr.clear()
    play_win = curses.newwin(0, 0, 0, 0)
    # Setup colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # Main loop
    play_win.nodelay(True)
    while True:
        draw_render(play_win, init_states)
        init_states = next_board_state(init_states)
        play_win.refresh()
        key = play_win.getch()
        if key == ord('q'):
            break
        time.sleep(args.time)
        

if __name__ == '__main__':
    args = print_arguments()
    init_states = []
    if args.file:
        try:
            init_states = load_board_state(args.file)
        except ValueError as e:
            raise e
    elif args.random:
        rows, cols = args.random
        init_states = random_state(rows, cols)
    else:
        args = print_arguments()
        
    draw(init_states)
