#!/usr/bin/env python3

"""Demo bot for CGI's Swedish Learders' conference 2017-12-01.
"""

import textwrap
import time

import telepot
from telepot.loop import MessageLoop

from enforsml.text import emlb, nlp, utils


bot_file = emlb.BotFile()
intents = bot_file.load("nextdemobot.emlb")

parser = nlp.Parser(intents)
debug=False

def debug_msg(msg):
    global debug

    if debug:
        print(msg)


def read_private(file_name):
    with open(file_name, "r") as f:
        contents = f.readline()
    return contents.strip()



def handle_msg(msg):
    global bot

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type != "text":
        return False

    user_txt = msg["text"].strip()
    user_id = msg["chat"]["id"]

    if len(user_txt) < 1:
        return False

    if user_txt[0] == "/":
        user_txt = user_txt[1:]

    print("Message from user:", user_txt)

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
            bot.sendMessage(chat_id, response)
        except IndexError:
            bot.sendMessage(chat_id, "Jag förstår tyvärr inte. "
                            "Kan du omformulera dig?")

    user_txt = ""


bot = telepot.Bot(read_private("private/telegram_token"))
print(bot.getMe())

MessageLoop(bot, handle_msg).run_as_thread()

while True:
    try:
        time.sleep(10)
    except (KeyboardInterrupt):
        print()
        raise SystemExit
