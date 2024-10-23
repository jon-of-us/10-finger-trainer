import numpy as np

ALPHABET = list("enisratdhulcgmobwfkzpüäßövjyxq")
additional = list(".,0123456789-!@#$%^&*()_+[]{}|;':\"<>?/\\")
ALPHABET += additional
WORDS = np.array(
    [
        line.strip().split("\t")[1]
        for line in open("german-words.txt", "r", encoding="utf-8").readlines()
    ]
)
WORDS = [word for word in WORDS if len(word) > 3]
# add additional characters to words
WORDS = np.concatenate([WORDS, additional])

N_INIT_CHARS = 7

NEW_CHAR_TIME = 1.2
TIME_FADE_FACTOR = 0.85
NEW_CHAR_FACTOR = 1.3

MAX_TIME = 2
LINE_LEN = 30
