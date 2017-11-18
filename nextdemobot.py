#!/usr/bin/env python3

"""Demo bot for CGI's Swedish Learders' conference 2017-12-01.
"""

import textwrap

from enforsml.text import emlb, nlp, utils


bot_file = emlb.BotFile()
intents = bot_file.load("nextdemobot.emlb")

parser = nlp.Parser(intents)
debug=False

def debug_msg(msg):
    global debug

    if debug:
        print(msg)


user_txt = "start"

while True:
    user_txt = utils.unify_sentence_dividers(user_txt)
    sentences = utils.normalize_and_split_sentences(user_txt)

    for sentence in sentences:
        sentence = utils.remove_junk_chars(sentence)

        results = parser.parse(sentence)

        debug_msg("ANSWER CANDIDATES:")
        for result in results:
            debug_msg("    [%3d] %s" % (result.score, result.intent.response_data))
        
        try:
            result = results[0]
            debug_msg("\nANSWER:")
            response = result.intent.response_data
            print("\n".join(textwrap.wrap(response)))
        except IndexError:
            print("Jag förstår tyvärr inte. Kan du omformulera dig?")

    user_txt = ""
    while len(user_txt) == 0:
        try:
            user_txt = input("> ")
        except (KeyboardInterrupt, EOFError):
            print()
            raise SystemExit


