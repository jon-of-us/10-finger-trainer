import numpy as np
import config as c


class State:
    def __init__(
        self, alphabet=c.ALPHABET, reference_words=c.WORDS, n_init_chars=c.N_INIT_CHARS
    ):
        self.alphabet = np.array(alphabet)
        self.n = len(alphabet)
        self.is_known = np.zeros(self.n)
        self.is_known[: min(n_init_chars, self.n)] = True

        self.time = np.ones(self.n) * -1e10
        self.time[: min(n_init_chars, self.n)] = c.MAX_TIME

        """ first reference words are alphabet """
        self.ref_words = np.array(reference_words)
        self.n_ref_words = len(reference_words)
        self.char_counts = np.array(
            [
                [word.lower().count(char) for char in alphabet]
                for word in reference_words
            ]
        )
        self.reference_word_lens = np.array([len(word) for word in reference_words])

    def sorted_words(self):
        """word represented by index"""

        word_ranks = (
            self.char_counts @ self.time / self.reference_word_lens
            + np.random.rand(self.n_ref_words) * c.MAX_TIME * 0.1
        )
        argsort = np.argsort(word_ranks)[::-1]
        # words = self.ref_words[argsort]
        # ranks = word_ranks[argsort]
        # all = list(zip(words, ranks))

        # alph_sort = np.argsort(self.rank)
        # ran = self.rank[alph_sort]
        # alp = self.alphabet[alph_sort]
        # all2 = list(zip(alp, ran))
        # pass
        for idx in argsort:
            yield self.ref_words[idx]

    def update_char(self, char, time_s):
        if not char in self.alphabet:
            return
        char_idx = np.where(self.alphabet == char)[0]
        if not self.is_known[char_idx]:
            return
        self.time[char_idx] *= c.TIME_FADE_FACTOR
        self.time[char_idx] += (1 - c.TIME_FADE_FACTOR) * time_s

        # add new chars
        if np.max(self.time) < c.NEW_CHAR_TIME:
            for i in range(self.n):
                if not self.is_known[i]:
                    self.is_known[i] = True
                    self.time[i] = c.MAX_TIME
                    break
