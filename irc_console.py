import math
import json
import socket

import config
shellname = config.shellname

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

    def on_host_state_update(self):
        try:
            data = self.host_socket.recv(2048).decode("UTF-8")
            host_state = json.loads(data)
        except:
            print("Not connected to a host")
        else:
            if data:
                self.env['channels'] = host_state['channels']
                self.env['scripts'] = host_state['scripts']
                self.env['script_vars'] = host_state['script_vars']
                
                return host_state['message']

def make_json(query_type=None, action=None, entity=None, target=None, message=None):
    return {
        'query type': query_type,
        'action': action,
        'entity': entity,
        'target': target,
        'message': message,
        'var_value': var_value
    }

def check_input(inp):
    if inp.find("$") == 0:
        print("python:", input[1:])
    
def init_env(shell, f):
    try:
        shell.host_socket.connect(('localhost', 8181))
        shell.on_connect()
    except Exception as e:
        print(e)
        print("Could not connect to a bot. Type \"host connect\" to try again.")

padding = 5
entries_per_line = 5

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

                    if com == "/chanoff":
                        shell.curr_chan = ""
                        
                    if com == "/c":
                        if shell.curr_chan != "":
                            shell.curr_com = make_json(query_type='server_action',\
                            action='PRIVMSG', \
                            entity=[shell.curr_chan],\
                            message=msg)
                        else:
                            print("Not on a channel")

                    if com == "/all":
                        shell.curr_com = make_json(query_type='server_action',\
                            action='PRIVMSG', \
                            entity=shell.env['channels'],\
                            message=msg)
                    

                if shell.curr_com != None:
                    with open(commandfile, "w") as c:  
                        c.write(shell.curr_com)
                    shell.curr_com = shell.curr_state

            except KeyboardInterrupt:
                print("\nCTRL+C was used; shell interrupted.")
                break