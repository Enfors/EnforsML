"""Natural language processing.
"""

from enforsml.text import ngram, bagofwords


class NLPError(BaseException):
    """Generic NLP error.
    """
    pass


class IncorrectArg(NLPError):
    pass


class Intent(object):
    """The intent behind a textual command or sentence.

    >>> intent = Intent("start")
    >>> intent
    Intent('start')
    >>> print(intent)
    'start' intent
    """

    def __init__(self, name, train_sentences=[], response_data=None):
        self.name = name
        self.train_sentences = train_sentences
        self.response_data = response_data
        self.ngram_matrix = ngram.NGramMatrix(1, 4)
        self.trained = False

    def __repr__(self):
        return "Intent('%s')" % str(self.name)

    def __str__(self):
        return "'%s' intent" % self.name

    def train(self):
        """Train the intent on recognizing the sentence.
        """

        if not type(self.train_sentences) is list:
            raise IncorrectArg("sentences is not alist")

        for sentence in self.train_sentences:
            self.ngram_matrix.add_sentence_value(sentence.lower(), 10)
        self.trained = True

    def check(self, sentence):
        if not self.trained:
            self.train()

        return self.ngram_matrix.get_sentence_values(sentence.lower())


class ScoredIntent(object):
    """A container for an Intent and a (confidence) score.

    >>> intent = Intent("default")
    >>> scored_intent = ScoredIntent(intent, 10)
    >>> scored_intent
    ScoredIntent(Intent('default'), 10)
    """

    def __init__(self, intent, score):
        self.intent = intent
        self.score = score

    def __repr__(self):
        return "ScoredIntent(%s, %d)" % (repr(self.intent), self.score)


class Parser(object):
    """Parses text and matches it to Intents.

    >>> parser = Parser()
    >>> parser
    Parser()
    >>> len(parser)
    0
    """

    def __init__(self, intents=[]):
        self.corpus = bagofwords.BagOfWords()
        self.intents = intents
        self.prepared = False

    def __repr__(self):
        return "Parser()"

    def __str__(self):
        return "Parser"

    def __len__(self):
        return len(self.intents)

    def prepare(self):

        for intent in self.intents:
            for sentence in intent.train_sentences:
                self.corpus.add_words(sentence.lower().split(" "))

        print("Prepared. Corpus contains %d words." % len(self.corpus))
#        num_words = len(corpus_bag)
#        for word, freq in corpus_bag.sorted_matrix():
#            print("%4d / %.2f%%: %s" % (freq, (freq/num_words) * 100, word))

        self.prepared = True

    def add_intents(self, new_intents):
        self.intents.extend(new_intents)

    def parse(self, txt):
        """Parse input from a user, and return a ParseResult object.
        """

        if not self.prepared:
            self.prepare()

        result = ParseResult()

        for intent in self.intents:
            score = sum(intent.check(txt))
            if score > 0:
                result.add(ScoredIntent(intent, score))

        result.sort()

        print("TF-IDF\n======")
        sub_corpus = bagofwords.BagOfWords()
        for sentence in result.scored_intents[0].intent.train_sentences:
            sub_corpus.add_words(sentence.lower().split(" "))
        tfidf_matrix = self.corpus.sorted_tfidf(sub_corpus)

        for k, v in tfidf_matrix:
            print("%f: %s" % (v, k))

        return result


class ParseResult(object):
    """The return value of a Parser's parse() function.
    It includes a list of Intents, sorted by their confidence score.

    >>> intent1 = Intent("Intent 1")
    >>> intent2 = Intent("Intent 2")
    >>> intent3 = Intent("Intent 3")
    >>> scored_intent1 = ScoredIntent(intent1, 20)
    >>> scored_intent2 = ScoredIntent(intent2, 10)
    >>> scored_intent3 = ScoredIntent(intent3, 30)
    >>> result = ParseResult([scored_intent1,
    ...    scored_intent2,
    ...    scored_intent3])
    >>> print(result)
    Scored intents
    ==============
     30: 'Intent 3' intent
     20: 'Intent 1' intent
     10: 'Intent 2' intent
    """

    def __init__(self, scored_intents=[]):
        self.scored_intents = scored_intents
        self.sort()

    def add(self, scored_intent):
        self.scored_intents.append(scored_intent)

    def sort(self):
        self.scored_intents = sorted(self.scored_intents,
                                     key=lambda i: i.score,
                                     reverse=True)

    def __str__(self):

        output = "Scored intents\n=============="

        for scored_intent in self.scored_intents:
            output += "\n%3d: %s" % (scored_intent.score, scored_intent.intent)

        return output

    def __len__(self):
        return len(self.scored_intents)

    def __getitem__(self, key):
        return self.scored_intents[key]
