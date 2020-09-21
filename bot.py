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

    # get calling module's filename
    def info(self):
        inspect = __import__('inspect')
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        return str(mod).split(r'\\')[-1].split('.')[0] 


def on_console_connect(bot, conn):
    ct = threading.Thread(target=cs.console_stuff, args=(bot, conn,))
    threads['console_thread'] = ct
    ct.start()


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
