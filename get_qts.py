## todo:
## Add more SFW image hosts

import random
import re
import time
import urllib
import urllib.request

class Cutie:
    """
    Gets random image from safebooru
    .qt fetches from random query
    .qt [tags] fetches using tags separated by spaces
    """

    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.curr_msg = None

    def get_env(self):
        return {}

    def get_command(self):
        msg = None

        if self.curr_msg.find("PRIVMSG #") != -1 and self.curr_msg.find(":.qt") != -1:
            if self.curr_msg.find("PRIVMSG #") != -1 and self.curr_msg.find("SLAPP_") != -1:
                return
            
            calling_channel = self.curr_msg[self.curr_msg.find("PRIVMSG #"):].split(" ")[1]
            com = self.curr_msg[self.curr_msg.find(":.qt"):].replace(":", "").replace("\r\n", "").split(" ")

            if com[0] == ".qt":
                if len(com) == 1:  # get random qt
                    msg = self.get_qt_url()

                else: # get qt by tags
                    com[-1] = com[-1].replace("\r\n", "")
                    msg = self.get_qt_url(com[1:])

            if msg:
                self.bot.send_msg(calling_channel, msg)