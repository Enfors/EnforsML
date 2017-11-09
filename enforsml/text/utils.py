import text.word

def normalize(text):
    """Return a normalized copy of text.
    """

    text = normalize_whitespace(text)
    text = unify_sentence_dividers(text)

    return text


def unify_sentence_dividers(text):
    """Return copy of text with ? and ! replaced with .
    """

    for ch in ["!", "?"]:
        text = text.replace(ch, ".")

    return text


def remove_junk_chars(text):
    """Return copy of text without unneeded chars.
    """

    for ch in [": ", "; "]:
        text = text.replace(ch, " ")

    for ch in [".", ",", "(", ")", '"']:
        text = text.replace(ch, "")

    return text


def remove_words(text, words_to_remove):
    """Return a copy of the text string with the specified words (not Words)
    removed.
    """

    output = ""

    for word in text.split(" "):
        if word not in words_to_remove:
            output += word + " "

    return output.strip()


def split_sentences(text):
    """Attempt to split a text into sentences.
    """

    text = normalize_whitespace(text)
    text.replace("!", ".")
    text.replace("?", ".")
    sentences = [sentence.strip() for sentence in text.split(". ")]

    sentences[-1] = sentences[-1].rstrip(".")

    return sentences


def split_sentence(txt):
    """Given a normalized sentence, return a list of Words.
    """

    words = []
    for part in txt.split(" "):
        words.append(text.word.Word(part))

    return words


def normalize_and_split_sentences(text):
    """Return normalized sentences.

    >>> normalize_and_split_sentences("Foo bar. Another small sentence.")
    ['Foo bar', 'Another small sentence']
    >>> normalize_and_split_sentences(" Foo bar. Another  small sentence.")
    ['Foo bar', 'Another small sentence']
    >>> normalize_and_split_sentences("Foo bar . Another  small sentence.")
    ['Foo bar', 'Another small sentence']
    """

    text = normalize(text)
    sentences = split_sentences(text)

    return sentences


def normalize_whitespace(text):
    """Return a copy of text with one space between all words, with all
    newlines and tab characters removed.

    >>> print(normalize_whitespace("some text"))
    some text
    >>> print(normalize_whitespace(" some text "))
    some text
    >>> print(normalize_whitespace(" some   text"))
    some text
    >>> print(normalize_whitespace('\t\tsome text'))
    some text
    >>> print(normalize_whitespace("  some       text "))
    some text
    """

    new_text = text.replace("\n", " ")
    new_text = new_text.replace("\r", "")
    new_text = new_text.replace("\t", " ")

    words = [word.strip() for word in new_text.split(" ") if len(word) > 0]
    new_text = " ".join(words)
    return new_text
