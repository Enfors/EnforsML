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
        """Return the contents of a "secret" file in the private/ directory.
        We do this to be able to have the secret telegram token in a file
        which is NOT in the source code - IE, we don't want the token to
        be publicly available on GitHub.
        """
        with open(file_name, "r") as f:
            contents = f.readline()
        return contents.strip()

    def handle_msg(self, msg):
        try:
            msg["message"]["chat"]
        except KeyError:
            print("Unknown message format.")
            return None

        msg = msg["message"]
        
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
                self.send_response(msg, response)
            except IndexError:
                self.send_response(msg, "Jag förstår tyvärr inte. "
                                   "Kan du omformulera dig?")

        user_txt = ""

    def send_msg(self, chat_id, text):
        self.bot.sendMessage(chat_id, text)

    def send_response(self, in_response_to_msg, text):
        print("Bot -> %s %s: %s" % (in_response_to_msg["from"]["first_name"],
                                    in_response_to_msg["from"]["last_name"],
                                    text))
        self.send_msg(in_response_to_msg["chat"]["id"], text)

    def run(self):
        self.bot = telepot.Bot(self.read_private("private/telegram_token"))

        # MessageLoop(self.bot, self.handle_msg).run_as_thread()

        update_id = None
        wait_time = 10  # Seconds to wait before retrying after an error
        
        while True:
            try:
                if not update_id:
                    all_msgs = self.bot.getUpdates()
                else:
                    all_msgs = self.bot.getUpdates(offset=update_id)

                if wait_time > 10:
                    print("Connection re-established.")
                    wait_time = 10
                
                for msg in all_msgs:
                    update_id = msg["update_id"] + 1
                    self.handle_msg(msg)
            except (KeyboardInterrupt):
                print()
                raise SystemExit
            except:
                print("Communication error, retrying in %d seconds." % wait_time)
                time.sleep(wait_time)
                wait_time *= 2
                if wait_time > 300:
                    wait_time = 300

            
if __name__ == "__main__":
    app = App()
    app.run()
