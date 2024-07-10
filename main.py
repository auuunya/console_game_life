#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/07/08 11:37:30
@Desc    :   None
'''

# here put the import lib
import random, os, time
from functools import reduce


ALIVE = 1
DIED = 0
ROW_CHARS = "-"
LINE_CHARS = "|"

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

def render(states):
    for index, row in enumerate(states):
        if index == 0:
            print ((len(row) * ROW_CHARS) + 2 * ROW_CHARS)
        var_char = LINE_CHARS
        for item in row:
            if item:
                var_char += "#"
            else:
                var_char += " "
        var_char += LINE_CHARS
        print (f"{var_char}")
        if index == len(states) - 1:
            print ((len(row) * ROW_CHARS) + 2 * ROW_CHARS)

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
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

if __name__ == '__main__':
    init_states = load_board_state("./toad.txt")
    while True:
        new_state = next_board_state(init_states)
        render(new_state)
        init_states = new_state
        time.sleep(0.5)
        os.system('clear' if os.name == 'posix' else 'cls')
