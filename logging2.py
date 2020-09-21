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

    def get_message(self, message):
        pass

    def log_stuff(self):
        if any(self.message_buffer):
            if len(self.message_buffer) >= self.bufsize:
                self.message_buffer = self.message_buffer[1:]

        if self.bot.message_queue[-1].find("PRIVMSG #")  != -1 or self.bot.message_queue[-1].find("MODE #") != -1:
            message = self.bot.message_queue[-1]
            self.message_buffer.append(message)

            if self.logging:
                with open("logtest.txt", 'a') as log:
                    log.write(message)