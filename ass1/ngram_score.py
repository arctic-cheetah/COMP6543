"""
Allows scoring of text using n-gram probabilities
17/07/12
"""

# Attribution from github:
# https://github.com/jameslyons/python_cryptanalysis.git
from math import log10


class NGramScore:
    def __init__(self, ngramfile, sep=" "):
        """Load an n-gram file of “key count” pairs and pre-compute log-probabilities."""
        self.ngrams = {}

        # Read the file (universal-newline friendly, explicit UTF-8 just in case)
        with open(ngramfile, "r", encoding="utf-8") as f:
            for line in f:
                key, count = line.strip().split(sep)
                self.ngrams[key] = int(count)

        # All keys are the same length, so grab the first one to set L
        self.L = len(next(iter(self.ngrams)))
        self.N = sum(self.ngrams.values())

        # Pre-compute log10 probabilities
        for key in list(self.ngrams):
            self.ngrams[key] = log10(self.ngrams[key] / float(self.N))

        # Log-probability to fall back on for unseen n-grams
        self.floor = log10(0.01 / float(self.N))

    def score(self, text: str) -> float:
        """Return the log-probability score for the supplied text."""
        score = 0.0
        lookup = self.ngrams.get  # local binding for speed
        L = self.L

        for i in range(len(text) - L + 1):
            ngram = text[i : i + L]
            score += lookup(ngram, self.floor)

        return score
