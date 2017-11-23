#!/usr/bin/env python3

"""Demo bot for CGI's Swedish Learders' conference 2017-12-01.
"""

from pprint import pprint

import textwrap
import time

import telepot
from telepot.loop import MessageLoop

from enforsml.text import emlb, nlp, utils


bot_file = emlb.BotFile()
intents = bot_file.load("nextdemobot.emlb")

parser = nlp.Parser(intents)


class App(object):

    def __init__(self, debug=False):
        self.debug = debug
    
    def debug_msg(self, msg):
        if self.debug:
            print(msg)

    def read_private(self, file_name):
        with open(file_name, "r") as f:
            contents = f.readline()
        return contents.strip()

    def handle_msg(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != "text":
            return False

        pprint(msg)
        user_txt = msg["text"].strip()
        user_id = msg["chat"]["id"]

        if len(user_txt) < 1:
            return False

        if user_txt[0] == "/":
            user_txt = user_txt[1:]

        print("Bot <- %s %s: %s" % (msg["from"]["first_name"],
                                    msg["from"]["last_name"],
                                    user_txt))

        user_txt = utils.unify_sentence_dividers(user_txt)
        sentences = utils.normalize_and_split_sentences(user_txt)

        for sentence in sentences:
            sentence = utils.remove_junk_chars(sentence)

            results = parser.parse(sentence)

            self.debug_msg("ANSWER CANDIDATES:")
            for result in results:
                self.debug_msg("    [%3d] %s" % (result.score, result.intent.response_data))
        
            try:
                result = results[0]
                self.debug_msg("\nANSWER:")
                response = result.intent.response_data
                self.debug_msg("    %s" % response)
                self.bot.sendMessage(chat_id, response)
            except IndexError:
                self.bot.sendMessage(chat_id, "Jag förstår tyvärr inte. "
                                     "Kan du omformulera dig?")

        user_txt = ""

    def run(self):
        self.bot = telepot.Bot(self.read_private("private/telegram_token"))

        MessageLoop(self.bot, self.handle_msg).run_as_thread()

        while True:
            try:
                time.sleep(10)
            except (KeyboardInterrupt):
                print()
                raise SystemExit

            
if __name__ == "__main__":
    app = App()
    app.run()
