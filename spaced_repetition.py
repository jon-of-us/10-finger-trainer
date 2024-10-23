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
        self.time[: min(n_init_chars, self.n)] = c.NEW_CHAR_TIME * c.NEW_CHAR_FACTOR

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
        args = np.argsort(self.time)[::-1]
        alph = self.alphabet[args]
        times = self.time[args]
        times = list(zip(alph, times))
        word_ranks = list(zip(self.ref_words[argsort], word_ranks[argsort]))
        pass
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
        
        max_time = np.max(self.time)
        if max_time < c.NEW_CHAR_TIME:
            for i in range(self.n):
                if not self.is_known[i]:
                    self.is_known[i] = True
                    self.time[i] = c.NEW_CHAR_TIME * c.NEW_CHAR_FACTOR
                    # print in green
                    print(
                        "\033[92m"
                        + "You unlocked a new character: "
                        + self.alphabet[i]
                        + "\n"
                        + "\033[0m"
                    )
                    break
