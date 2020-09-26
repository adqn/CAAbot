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