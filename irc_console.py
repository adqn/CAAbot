import math
import json
import socket

shellname = "CAAbot"

class IRCShell:
    def __init__(self, host_socket):
        self.host_socket = host_socket

        self.env = {
            'channels': "",
            'current_channel': "",
            'scripts': [],
        }
        
        self.action = "default"
        self.curr_com = None
        self.curr_chan = ""
        self.curr_chan_id = 1

    def on_connect(self):
        try:
            data = self.host_socket.recv(2048).decode("UTF-8")
            host_state = json.loads(data)
        except:
            print("Not connected to a host")
        finally:
            if data:
                self.env['channels'] = host_state['channels']
                self.env['scripts'] = host_state['scripts']

def make_json(query_type=None, action=None, entity=None, target=None, message=None):
    return {
        'query type': query_type,
        'action': action,
        'entity': entity,
        'target': target,
        'message': message,
    }

def check_input(inp):
    if inp.find("$") == 0:
        print("python:", input[1:])

# Change to sqlite db checking or something
def check_config(f):
    try:
        with open(f) as conf:
            config = conf.readlines()
            channels = config[0].replace("\n", "").split(' ')[1:]

            return {
                'channels': channels,
            }
    except:
        pass
    
def init_env(shell, f):
    try:
        shell.host_socket.connect(('localhost', 8181))
        shell.on_connect()
    except Exception as e:
        print(e)
        print("Could not connect to a bot. Type \"host connect\" to try again.")

if __name__ == '__main__':
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    shell = IRCShell(host)
    init_env(shell)

    while True:
        shell.curr_com = None

        try:
            if shell.curr_chan != "":
                indicator = "@"
            else:
                indicator = ""

            inp = str(input("%s%s%s> " % (shellname, indicator, shell.curr_chan)))

            if len(inp) > 0:
                if inp[0] == "/":   
                    com = inp.split(" ")[0]
                    msg = " ".join(inp.split(" ")[1:])
                    
                    if com == "/next":
                        if any(shell.env['channels']):
                            if shell.curr_chan_id == len(shell.env['channels']):
                                shell.curr_chan_id = 1
                            else:
                                shell.curr_chan_id += 1
                            shell.curr_chan = shell.env['channels'][shell.curr_chan_id - 1]  

                    if com == "/c":
                        if shell.curr_chan != None:
                                shell.curr_com = "\n".join([shell.curr_chan, msg])
                        else:
                            pass

                    if com == "/next":
                        if shell.curr_chan_id == len(shell.env['channels']):
                            shell.curr_chan_id = 1
                        else:
                            shell.curr_chan_id += 1
                        shell.curr_chan = shell.env['channels'][shell.curr_chan_id - 1]         

                    if com == "/all":
                        shell.curr_com = "\n".join([" ".join(shell.env['channels']), msg])
                    

                if shell.curr_com != None:
                    with open(commandfile, "w") as c:  
                        c.write(shell.curr_com)
                    shell.curr_com = shell.curr_state

            except KeyboardInterrupt:
                print("\nCTRL+C was used; shell interrupted.")
                break