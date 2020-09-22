import re
import time
import numpy as np

class Quotes:
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.curr_msg = None

    def get_command(self):
        if self.curr_msg.find('PRIVMSG #') != -1:
            prefix = self.curr_msg.split('PRIVMSG ')[1]
            entity = prefix.split(' ')[0]
            message = self.curr_msg.split('PRIVMSG', 1)[1].split(':')[1]

            if message.find('.q') == 0:
                if message == '.q':
                    random_quote = self.random_quote().replace("\n", "")
                    self.bot.send_msg(entity, random_quote)

                elif message.find('.q add') == 0:
                    message = message.split('.q add ')[1]
                    username = message.split(' ', 1)[0]
                    quote = message.split(' ', 1)[1]

                    self.add_quote(username, quote)
                    self.bot.send_msg(entity, "Quote added.")

                else:
                    if re.findall('.q \w*', message):
                        username = message.split('.q ')[1]
                        self.bot.send_msg(entity, self.random_quote(username).replace("\n", ""))

    def add_quote(self, user, message):
        quote = '<' + user + '> ' + message
        with open('db/user_quotes.txt', 'a+') as quotefile:
            quotefile.write(quote)

    def random_quote(self, username=None):
        with open('db/user_quotes.txt') as quotefile:
            quotes = [q for q in quotefile.readlines() if q != "\n"]

        #print(quotes)
        qsize = len(quotes)
        random_q = np.random.randint(0, qsize)

        if username:  # get random quote from user
            name_formatted = '<' + username + '>'

            while quotes[random_q].find(name_formatted) != 0:
                random_q = np.random.randint(0, qsize)
                
            random_quote = quotes[random_q]
            print(random_quote)

        else:  # get random quote
            random_quote = quotes[random_q]

        return random_quote

    def random_qdb(self):
        True

    def main_thread(self):
        while self.running:
            if self.bot.script_msg_switches['userquotes']:
                self.curr_msg = self.bot.message_queue[-1]
                self.get_command()

                self.bot.script_msg_switches['userquotes'] = False
            time.sleep(.5)

def get_instance(bot=None):
    if bot:
        quotes = Quotes(bot)
        quotes.running = True
        return quotes
    return None