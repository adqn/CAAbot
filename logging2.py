import time

class Logger:
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.logfile = None
        self.logging = False
        self.channels = []

        self.new_chats = True
        self.new_msg = None

        self.message_buffer = []
        self.bufsize = 50
        self.bufcount = 0

    def get_env(self):
        return {
            'running': self.running,
            'logfile': self.logfile,
            'logging': self.logging,
            'bufsize': self.bufsize,
            'current channels': self.bot.channels.copy()
        }
