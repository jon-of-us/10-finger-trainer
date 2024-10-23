import numpy as np
import config as c


class State:
    def __init__(self, alphabet, reference_words):
        self.alphabet = np.array(alphabet)
        self.n = len(alphabet)
        self.is_known = np.zeros(self.n)
        self.is_known[: min(c.N_INIT_CHARS, self.n)] = True
        self.ease = np.ones(self.n) * c.INITIAL_EASE
        # infinite rank for unknown words
        self.rank = np.ones(self.n) * 1e9
        self.rank[: min(c.N_INIT_CHARS, self.n)] = c.INITIAL_RANK

        """ first reference words are alphabet """
        self.ref_words = np.array(reference_words)
        self.n_ref_words = len(reference_words)
        self.char_counts = np.array(
            [[word.count(char) for char in alphabet] for word in reference_words]
        )
        self.reference_word_lens = np.array([len(word) for word in reference_words])

    def sorted_words(self):
        """word represented by index"""

        word_ranks = (
            self.char_counts @ self.rank / self.reference_word_lens
            + np.random.rand(self.n_ref_words)
        )
        argsort = np.argsort(word_ranks)
        min_rank = word_ranks[argsort[0]]
        if min_rank > c.NEW_CHAR_RANK:
            for i in range(self.n):
                if not self.is_known[i]:
                    self.is_known[i] = True
                    self.rank[i] = c.INITIAL_RANK
                    break
        for idx in argsort:
            yield self.ref_words[idx]

    def update_char(self, char, time_s):
        char_idx = np.where(self.alphabet == char)[0]
        if not char in self.alphabet or not self.is_known[char_idx]:
            return
        self.rank[char_idx] = self.rank[char_idx] * self.ease[char_idx]
        time_s = max(c.PERFECT_TIME_S, min(c.FORGOT_TIME_S, time_s))
        badness = (time_s - c.PERFECT_TIME_S) / (c.FORGOT_TIME_S - c.PERFECT_TIME_S)
        badness = max(0, min(1, badness))
        ease = self.ease[char_idx] + 0.1 - badness * 5 * (0.08 + 5 * badness * 0.02)
        ease = max(1.3, min(2.5, ease))
        self.ease[char_idx] = ease


# s = State(list("abc"), ["ab", "ac", "bc", "abc", "bac", "cab"])
# if __name__ == "__main__":
#     while True:
#         word_idx = s.word_argsort()
#         print("next word: ", s.ref_words[word_idx])
#         for char in s.ref_words[word_idx]:
#             print(char)
#             time_s = float(input("time_s: "))
#             char_idx = np.where(s.alphabet == char)[0]
#             s.update_char(char_idx, time_s)
