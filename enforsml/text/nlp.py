"""Natural language processing.
"""


class Intent(object):
    """The intent behind a textual command or sentence.

    >>> intent = Intent("start")
    >>> intent
    Intent('start')
    >>> print(intent)
    'start' intent
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Intent('%s')" % str(self.name)

    def __str__(self):
        return "'%s' intent" % self.name


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
        self.intents = intents

    def __repr__(self):
        return "Parser()"

    def __str__(self):
        return "Parser"

    def __len__(self):
        return len(self.intents)
    

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

    def __init__(self, intent_scores):
        self.scored_intents = intent_scores
        self.sort()

    def sort(self):
        self.scored_intents = sorted(self.scored_intents, key=lambda i: i.score,
                                     reverse=True)

    def __str__(self):

        output = "Scored intents\n=============="

        for scored_intent in self.scored_intents:
            output += "\n%3d: %s" % (scored_intent.score, scored_intent.intent)

        return output
                    
