import numpy as np

ALPHABET = list("enisratdhulcgmobwfkzpüäßövjyxq")
additional = list("0123456789.,-!@#$%^&*()_+[]{}|;':\"<>?/\\")
ALPHABET += additional
WORDS = np.genfromtxt(
    "german-word-list-total.csv", delimiter="\t", dtype=str, encoding="utf-8"
)[:5000, 1]
# add additional characters to words
WORDS = np.concatenate([WORDS, additional])

N_INIT_CHARS = 5

INITIAL_EASE = 2.5
INITIAL_RANK = 1.0
NEW_CHAR_RANK = 20

FORGOT_TIME_S = 2
PERFECT_TIME_S = 0.2
LINE_LEN = 30
