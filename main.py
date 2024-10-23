from spaced_repetition import State
import pickle
import os
import config as c
from msvcrt import getwch
import time
import numpy as np


# load state
for file in os.listdir("./"):
    if file == "state.pkl":
        state = pickle.load(open("state.pkl", "rb"))
        break
else:
    state = State(c.ALPHABET, c.WORDS)


# main loop
while True:
    # generate line

    line = ""
    for word in state.sorted_words():
        if len(line) + len(word) < c.LINE_LEN:
            line += word + " "
        else:
            break
    line = line.strip()
    line = " " + line
    line += "↩"
    # print line fat
    print("\033[1m" + line + "\033[0m")

    input_chars = []
    is_perfect_run = True
    last_time = time.time()
    while len(input_chars) < len(line):
        char = getwch()
        if char == "\x03":  # Ctrl+C sends ASCII 3 (ETX)
            print()
            print("Ciao!")

            # save state
            pickle.dump(state, open("state.pkl", "wb"))
            exit()
        # ignore enter
        elif char == "\x08":
            if len(input_chars) > 0:
                print("\x08 \x08", end="", flush=True)
                input_chars.pop()
        else:
            if char == "\r":
                char = "↩"
            now = time.time()
            is_correct = char == line[len(input_chars)]
            is_perfect_run = is_perfect_run and is_correct
            time_diff = (now - last_time) if is_correct else c.MAX_TIME
            last_time = now
            # force last enter
            if len(input_chars) == len(line) - 1 and not is_correct:
                continue
            input_chars.append((char, time_diff, is_correct))
            if is_correct:
                print(char, end="", flush=True)
            else:
                # print with red background
                print("\033[41m" + char + "\033[0m", end="", flush=True)

    if is_perfect_run:
        # perfect run in green letters on normal background
        print("\033[32m" + "\nPerfect run!" + "\033[0m", end="")
    print("\n")

    # update state
    for char, time_s, _ in input_chars:
        state.update_char(char, time_s)
    pickle.dump(state, open("state.pkl", "wb"))
