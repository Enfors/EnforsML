#!/usr/bin/env python3

"""Classes and functions related to n-grams.
"""

import doctest

from text import utils


class NGram(object):
    """The ngram class stores an n-gram.

    Given a list of Words, an n-gram is created. If a list of two Words
    is provided, a bi-gram is created. If three Words are provided, a
    3-gram is created, and so on.

    >>> from text.word import *
    >>> word1 = Word("some")
    >>> word2 = Word("words")
    >>> bi_gram = NGram([word1, word2])
    >>> bi_gram
    NGram([Word('some', word_type=1), Word('words', word_type=1)])
    >>> print(bi_gram)
    some words
    >>> len(bi_gram)
    2

    We can also do comparisons:

    >>> word1 = Word("one")
    >>> word2 = Word("two")
    >>> word3 = Word("one")
    >>> ngram1 = NGram([word1, word2])
    >>> ngram2 = NGram([word3, word2])
    >>> ngram1 == ngram2
    True
    >>> ngram3 = NGram([word1, word2, word3])
    >>> ngram1 == ngram3
    False
    """

    def __init__(self, words):
        if not words:
            words = []
        else:
            self.words = words

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return "NGram(%s)" % self.words

    def __str__(self):
        output = ""

        for word in self.words:
            output = output + str(word) + " "

        return output.strip()

    def __eq__(self, other_ngram):
        if len(self) != len(other_ngram):
            return False

        for i in range(0, len(self.words)):
            if self.words[i] != other_ngram.words[i]:
                return False

        return True


class NGramMatrix(object):
    """A list of dicts, where each dict will hold NGrams.
    """

    def __init__(self, min_n, max_n):
        self.min_n = min_n
        self.max_n = max_n
        self.matrix = []

        for n in range(0, max_n + 1):
            self.matrix.append({})

    def set_sentence_value(self, sentence, value):
        """Give a value to a sentence, and all its ngrams.
        """

        for n in range(self.min_n, self.max_n + 1):
            ngrams = make_ngrams(utils.split_sentence(sentence), n)

            for ngram in ngrams:
                dict_key = str(ngram)

                try:
                    ngram_values = self.matrix[n][dict_key]
                except KeyError:
                    ngram_values = []

                ngram_values.append(value)
                self.matrix[n][dict_key] = ngram_values

    def get_sentence_value(self, sentence):
        """Get the value for a sentence.
        """

        all_values = []

        for n in range(self.min_n, self.max_n + 1):
            ngrams = make_ngrams(utils.split_sentence(sentence), n)

            for ngram in ngrams:
                dict_key = str(ngram)
                value_sum = 0

                try:
                    values = self.matrix[n][dict_key]
                    for value in values:
                        value_sum = value_sum + value

                        avg = value_sum / len(values)

                    # Multiply the average with n, to weigh it.
                    # 3-gram matches are three times more significant than
                    # unigram matches.
                    all_values.append(avg * n)
                except KeyError:
                    pass  # This ngram didn't exist

        try:
            avg = sum(all_values) / len(all_values)
        except ZeroDivisionError:
            avg = 0

        return avg


def make_ngrams(words, n):
    """Return n-grams from a list of Words.
    """

    num_words = len(words)
    index = 0
    n_grams = []

    while index + n <= num_words:
        n_gram = NGram(words[index:index + n])
        n_grams.append(n_gram)
        index = index + 1

    return n_grams


def run_doctests():
    doctest.testmod()
