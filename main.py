from spaced_repetition import State
import numpy as np
import pickle
import os
import config as c
from msvcrt import getwche, getwch
import time


# load state
for file in os.listdir("./"):
    if file == "state.pkl":
        state = pickle.load(open("state.pkl", "rb"))
        break
else:
    state = State(c.ALPHABET, c.WORDS)


while True:

    # generate line
    line = []
    for word in state.sorted_words():
        if sum(len(w) + 1 for w in line) + len(word) < c.LINE_LEN:
            line.append(word)
        else:
            break
    line_str = " ".join(line)
    # print line fat
    print("\033[1m" + line_str + "\033[0m")

    input_chars = []
    is_perfect_run = True
    last_time = time.time()
    while len(input_chars) < len(line_str):
        char = getwch()
        if char == "\x03":  # Ctrl+C sends ASCII 3 (ETX)
            print()
            print("Ciao!")

            # save state
            pickle.dump(state, open("state.pkl", "wb"))
            exit()
        # ignore enter
        elif char == "\r":
            continue
        elif char == "\x08" and len(input_chars) > 0:
            print("\x08 \x08", end="", flush=True)
            input_chars.pop()
        else:
            now = time.time()
            is_correct = char == line_str[len(input_chars)]
            is_perfect_run = is_perfect_run and is_correct
            time_diff = (now - last_time) if is_correct else c.FORGOT_TIME_S
            last_time = now
            input_chars.append((char, time_diff, is_correct))
            if is_correct:
                print(char, end="", flush=True)
            else:
                # print with red background
                print("\033[41m" + char + "\033[0m", end="", flush=True)

    if is_perfect_run:
        # perfect run in green letters on normal background
        print("\033[32m" + "\nPerfect run!\n" + "\033[0m")
    else:
        print("\n")

    # update state
    for char, time_s, _ in input_chars:
        state.update_char(char, time_s)
    pickle.dump(state, open("state.pkl", "wb"))

    
