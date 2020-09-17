import json
import re
import time
import socket
import numpy as np
import select
import queue
import threading

import MySQLdb as db

import importlib
from importlib import reload

import config

threads = {}

class Bot:
    def __init__(self, irc):
        self.irc = irc
        self.dbp = None

        self.running = False
        self.channels = []
        self.current_scripts = {}

        self.script_state_update = True        
        self.script_msg_switches = {}

        self.new_msg = False
        self.message_queue = []
        self.suppress = ["PING :"]

        self.current_command = None

        self.logging = True
        self.log_file = False
        self.other_stuff = True

    def connect(self, server, port):
        print("username:", config.botnick)
        print("Connecting to " + server + " on port " + str(port))

        try:
            self.irc.connect((server,  port))
            self.irc.send(bytes("USER " + "test test test :test\n", "UTF-8"))
            self.irc.send(bytes("NICK " + config.botnick + "\n", "UTF-8"))
        except Exception as e:
            print("Could not connect to server.")

        print("Connection successful.")
        self.running = True
        time.sleep(3)

    def send_msg(self, entity=None, message=None):
        if entity:
            message = "PRIVMSG " + entity + " :" + message + "\n"

        self.irc.send(bytes(message + "\n", "UTF-8"))

    def join_channel(self, channel):
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

        resp = ""

        while resp.find("End of /NAMES list.") == -1:
            resp = self.get_resp()
            # print(resp)

            if resp.find("End of /NAMES list.") != -1:
                print("Joined channel " + channel)
                break

        time.sleep(1)

    def part_channel(self, channel):
        try:
            self.irc.send(bytes("PART " + channel + "\n", "UTF-8"))
            self.channels.remove(channel)
        except:
            pass

    def get_resp(self):
        resp = self.irc.recv(2048).decode("UTF-8")

        if resp.find('PING') != -1:
            self.irc.send(bytes("PONG :pingis\n", "UTF-8"))

        # initial PONG <number> response required by irc.rizon.net
        if resp.find('/QUOTE') != -1:
            index = resp.find('PONG')
            self.irc.send(bytes(resp[index:] + "\n", "UTF-8"))

            # put this in the initilization
            if config.password:
                print("Identifying with NICKSERV...")
                self.send_msg("NICKSERV", "identify " + config.password)
                time.sleep(3)

            return 1

        # change this to be more efficient
        # also push formatted messages to queue
        
        if resp.find("PRIVMSG #") != -1:
            prefix = resp.split('PRIVMSG ')[1]
            entity = prefix.split(' ')[0]
            message = resp.split("PRIVMSG", 1)[1].split(":")[1]
        
        if any(self.message_queue):
            if len(self.message_queue) >= 20:
                self.message_queue = self.message_queue[1:]
        
        return resp
    def get_command(self, entity, message):
        # user-quote functions
        if message.find(".q") == 0:
            if message == ".q":
                random_quote = self.random_quote()
                self.send_msg(entity, random_quote + "\n")

            elif message.find(".q add") == 0:
                message = message.split(".q add ")[1]
                username = message.split(' ', 1)[0]
                quote = message.split(' ', 1)[1]

                self.add_quote(username, quote)
                self.send_msg(entity, "Quote added.\n")

            else:
                if re.findall(".q \w*", message):
                    username = message.split(".q ")[1]
                    random_quote = self.random_quote(username)
                    self.send_msg(entity, random_quote + "\n")

        # add an admin username for this lol
        if message == ".admin quit":
            self.running = False

    def add_quote(self, user, message):
        quotefile = open("db/user_quotes.txt", "a+")
        quote = "<" + user + "> " + message + "\n"
        quotefile.write(quote)
        quotefile.close()

    def random_quote(self, username=None):
        quotefile = open("db/user_quotes.txt")
        quotearr = quotefile.readlines()
        quotefile.close()

        if username:  # get random quote from user
            userquotes = []

            for quote in quotearr:
                if quote.find("<" + username + ">") == 0:
                    userquotes.append(quote)

            userquotelen = len(userquotes) - 1

            if userquotelen > 0:
                random_quote = quotearr[np.random.randint(0, userquotelen)]
            else:
                random_quote = userquotes[userquotelen]

        else:  # get random quote
            quotelen = len(quotearr) - 1

            random_quote = quotearr[np.random.randint(0, quotelen)]

            while random_quote == '\n':
                random_quote = quotearr[np.random.randint(0, quotelen)]

        return random_quote

    def random_qdb(self):
        True

if __name__ == "__main__":
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    params = get_config("config.txt")

    bot = Bot(irc)
    bot.running = True
    bot.channels.append(params['channel'])
    bot.connect(params['server'], params['port'], params['botnick'])

    # bot.get_resp()

    while bot.running:
        print(bot.get_resp())
        time.sleep(.5)
