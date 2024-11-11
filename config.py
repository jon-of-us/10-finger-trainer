import numpy as np

ALPHABET = list("enisrtadhulcgmobwfkzpüäßövjyxq")
additional = list(".,0123456789-!?:';@\"()/#$%^&*_+[]{}|<>\\")
ALPHABET += additional

# add additional characters to words
words = additional
for line in open("german-words.txt", "r", encoding="utf-8").readlines():
    word = line.strip().split("\t")[1]
    # ignore short words
    if len(word) <= 3:
        continue
    # ignore words that have characters which are not in alphabet
    n_not_in_alph = sum(0 if char in ALPHABET else 1 for char in word)
    if n_not_in_alph > 0:
        continue
    if word.capitalize() == word:
        continue
    words.append(word)
    

WORDS = np.array(words)

N_INIT_CHARS = 5

NEW_CHAR_TIME = 0.6
TIME_FADE_FACTOR = 0.9
NEW_CHAR_FACTOR = 1.3

MAX_TIME = 2
LINE_LEN = 30
