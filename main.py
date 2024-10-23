from spaced_repetition import State
import numpy as np
import pickle
import os
import config as c
from read_char import getch


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

    # print line
    
    print(" ".join(line))
    input()
    
