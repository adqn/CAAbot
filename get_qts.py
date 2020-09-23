## Disclaimer:
##      Created by request from the community
##      I have no idea what safebooru is
##
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

    def get_qt_url(self, tags=None):
        qt_res = None
        qt_lines = []
        qt_line = None
        qt_url = None

        try:
            if tags:
                tags = ("+").join(tags)
                qt_query = "https://safebooru.org/index.php?page=post&s=list&tags=" + tags
                qt_link = self.get_random_pid(qt_query)
                qt_res = list(urllib.request.urlopen(qt_link)).copy()
                
                for line in qt_res:
                    if line.find(b'href="index.php?page=post&amp;s=view&amp;id') != -1:
                        qt_line = line
                        qt_lines.append(line.decode())

                if not qt_line:
                    return "No cuties found!"

                qt_lines = [l.split('"')[7].replace("amp;", "") for l in qt_lines]
                qt = qt_lines[random.randrange(0, len(qt_lines) + 1)]
                qt_url = "https://safebooru.org/" + qt

            else:
                qt_res = list(urllib.request.urlopen("https://safebooru.org/index.php?page=post&s=random")).copy()
                
                for line in qt_res:
                    if line.find(b'<meta property="og:image" itemprop="image" content="') != -1:
                        qt_line = line
                
                if qt_line:
                    qt_url = qt_line.split(b'"')[5].decode()

        except Exception as e:
            print(e)

        if qt_url:
            return qt_url                

    def get_random_pid(self, qt_query):
        paginator = None
        qt_res = list(urllib.request.urlopen(qt_query)).copy()

        for line in qt_res:
            if line.find(b'pid=') != -1:
                paginator = line.decode()

        if paginator:
            pids = re.findall(r'pid=[0-9]+', paginator)
            pid_max = int(pids[-1].replace("pid=", ""))
            pid = random.randrange(0, pid_max, 40)

        else:
            pid = 1

        page = qt_query + "&pid=" + str(pid)
        return page

    def main_thread(self):
        while self.running:
            if self.bot.script_msg_switches['get_qts'] :
                self.curr_msg = self.bot.message_queue[-1]
                self.get_command()
                self.bot.script_msg_switches['get_qts'] = False

            time.sleep(.2)

def get_instance(bot=None):
    if bot:
        qts = Cutie(bot)
        qts.running = True
        return qts
    return None