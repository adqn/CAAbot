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