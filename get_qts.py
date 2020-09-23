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

