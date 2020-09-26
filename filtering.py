import re
import time

class Filter:
    """
    Various functions for filtering messages and performing actions
    based on filter parameters.
    """

    def __init__(self, bot):
        self.bot = bot
        self.name = bot.info()
        self.running = False
        self.channels = bot.channels.copy()
        self.new_chats = False
        self.new_msg = None
        self.curr_msg = None

        self.silent_mode_on = False
        self.silenced_users = []
        self.altered_modes = {}

    def get_env(self):
        return {}

    def auto_reply(self):
        bufsize = 7 # Amount of messages to get per call

        try:
            temp_buffer = self.bot.message_queue[-bufsize:]

            for m in temp_buffer:         
                for string in filter_list:       
                    if m.find(string) != -1:        
                        filter_list[string][1] += 1
                    else:
                        filter_list[string][1] = 0
                
            for string in filter_list:
                if filter_list[string][1] == filter_list[string][2]:
                    channel = filter_list[string][0]
                    self.bot.send_msg(channel, filter_list[string][3])

                filter_list[string][1] = 0
            
        except Exception as e:
            print("what the", e)
    
    # Reverses any modes set on channels/users
    def auto_set_modes(self):
        channel = None

        try:
            user = self.curr_msg.split(" ")[0][1:]
            username = self.curr_msg.split(" ")[0][1:].split("!")[0]
            prefix = self.curr_msg.split('MODE ')[1]
            channel = prefix.split(' ')[0]
            mode = self.curr_msg.split("PRIVMSG", 1)[1].split(":")[1]

        except:
            pass

        if channel:
            if channel in mode_filters:
                pass                

            #q = "MODE " + channel + " +b"
            name = "testname"

            if self.curr_msg.find("+o " + testname) != -1:
                index = self.curr_msg.find("+o " + testname)
                tmp = self.curr_msg[index:].split(" ")[1]
                msg = "MODE " + channel + " -o " + tmp
                self.bot.send_msg(message=msg)

            if self.curr_msg.find(q) != -1:
                index = self.curr_msg.find(q)
                tmp = self.curr_msg[index:].split(" ")[3]
                msg = "MODE " + channel + " -b " + tmp + "!*@*"
                #self.bot.send_msg(message=msg)

            banlist = {}

            if self.curr_msg.find("JOIN :") != -1:
                for f in banlist:
                    if f in user:
                        msg = "MODE " + channel + " +b" + username
                        self.bot.send_msg(message=msg)


    def main_thread(self):
        while self.running:
            if self.bot.script_msg_switches['filtering']:
                self.curr_msg = self.bot.message_queue[-1]

                self.auto_reply()
                self.auto_set_modes()
                self.silent_mode()

                self.bot.script_msg_switches['filtering'] = False
            time.sleep(0.5)

def get_instance(bot=None):
    if bot:
        bot.info()
        filter = Filter(bot)
        filter.running = True
        return filter
    return None