import re
import time
import socket
import numpy as np

class Bot:
  def __init__(self, irc):
    self.irc = irc
    self.running = False
    self.channels = []
    self.commands = {
        '.qdb': "random_qdb",
      }

  def connect(self, server, port, botnick):
    print("Connecting to " + server + " on port " + str(port))

    self.irc.connect((server, int(port)))
    self.irc.send(bytes("USER test test test :test\n", "UTF-8"))
    self.irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))


    print("Connection successful.")
    time.sleep(3)

  def send_msg(self, entity, message):
    msg = "PRIVMSG " + entity + " :" + message + "\n"
    self.irc.send(bytes(msg, "UTF-8"))
  
  def join_channel(self, channel):
    self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    resp = ""

    while resp.find("End of /NAMES list.") == -1:
      resp = self.get_resp()
      #print(resp)

      if resp.find("End of /NAMES list.") != -1:
        print("Joined channel " + channel)
        break
    
    time.sleep(1)

  # all commands/server requests parsed and handled from here
  def get_resp(self):
    resp = self.irc.recv(2048).decode("UTF-8")
    
    if resp.find('PING') != -1:
      self.irc.send(bytes("PONG :pingis\n", "UTF-8"))

    # initial PONG <number> response required by irc.rizon.net
    if resp.find('/QUOTE') != -1:
      index = resp.find('PONG')
      self.irc.send(bytes(resp[index:] + "\n", "UTF-8"))

      # put this in the initilization
      self.join_channel(self.channels[0])

    # change this to be more efficient
    if resp.find("PRIVMSG #") != -1:
      prefix = resp.split('PRIVMSG ')[1]
      entity = prefix.split(' ')[0]
      message = resp.split("PRIVMSG", 1)[1].split(":")[1]
      if message[0] == ".":
        #print("got command? " + message)
        self.get_command(entity, message.strip("\n\r"))

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

    else: # get random quote
      quotelen = len(quotearr) - 1

      random_quote = quotearr[np.random.randint(0, quotelen)]

      while random_quote == '\n':
        random_quote = quotearr[np.random.randint(0, quotelen)]

    return random_quote

  def random_qdb(self):
    True


def get_config(configfile):
  config = open(configfile).readlines()

  server = config[0].split(' ')[1]
  port = config[0].split(' ')[2]
  channel = config[1].split(' ')[1]
  botnick = config[2].split(' ')[1]

  return {'server': server, 'port': port, 'botnick': botnick, 'channel': channel}


if __name__ == "__main__":
  irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  params = get_config("config.txt")

  bot = Bot(irc)
  bot.running = True
  bot.channels.append(params['channel'])
  bot.connect(params['server'], params['port'], params['botnick'])

  #bot.get_resp()

  while bot.running:
    print(bot.get_resp())
    time.sleep(.5)