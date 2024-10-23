import numpy as np

ALPHABET = list("enisratdhulcgmobwfkzpüäßövjyxq")
additional = list("0123456789.,-!@#$%^&*()_+[]{}|;':\"<>?/\\")
ALPHABET += additional
WORDS = np.genfromtxt(
    "german-word-list-total.csv", delimiter="\t", dtype=str, encoding="utf-8"
)[:, 1]
# add additional characters to words
WORDS = np.concatenate([WORDS, additional])

N_INIT_CHARS = 7

NEW_CHAR_TIME = 0.6
TIME_FADE_FACTOR = 0.85
NEW_CHAR_FACTOR = 1.3

MAX_TIME = 2
LINE_LEN = 30
