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
                            
                    if com == '/mode':
                        shell.curr_com = make_json(query_type='server_action', \
                            action='mode', \
                            message=inp.replace("/mode", "MODE"))

                    if com == "/disconnect" or com == "/connect":
                        shell.curr_com = make_json(query_type='bot_action', action=inp[1:])

                    if com == "/msg":
                        shell.curr_com = make_json(query_type='server_action',\
                        action='PRIVMSG', \
                        entity=[inp.split(" ")[1]],\
                        message=" ".join(inp.split(" ")[2:]))                        

                    if com == "/join":
                        if msg != "":
                            for chan in inp.split(" ")[1:]:
                                if chan not in shell.env['channels']:
                                    shell.env['channels'].append(chan)
                                    shell.curr_com = {'query type': 'server_action',
                                                    'action': com,
                                                    'target': inp.split(" ")[1:]}                   

                    if com == "/part":
                        if msg != "":
                            for chan in inp.split(" ")[1:]:
                                if chan in shell.env['channels']:
                                    shell.env['channels'].remove(chan)

                            shell.curr_com = {'query type': 'server_action',
                                            'action': com,
                                            'target': inp.split(" ")[1:]}                                                         

                    if com == "/users":
                        shell.curr_com = {
                            'query type': 'server_action',
                            'action': com,
                            'message': inp.replace("/users", "NAMES")
                        }

                if inp[0] != "/":
                    com = inp.split(" ")[0]
                    msg = inp.split(" ")[1:]

                    if com == "chans":
                        if len(shell.env['channels']) > 0:
                            print("Current channels:\n", " ".join(shell.env['channels']))
                        else:
                            print("Not on any channels")                        
                            
                    if com == "load":
                        if any(msg):
                            shell.curr_com = make_json(query_type="bot_action", \
                                action='load script', \
                                target=msg[0])

                    if com == "reload":
                        if any(msg):
                            shell.curr_com = make_json(query_type="bot_action", \
                                action='reload script', \
                                target=msg[0])                                

                    if com == "scripts":
                        scripts = shell.env['scripts']
                        entries_most = math.ceil(len(shell.env['scripts'])/entries_per_line)
                        print("Currently running scripts:")
                        for i in range(entries_most):
                            output = ", ".join(scripts[i*entries_per_line:(i+1)*(entries_per_line)])
                            print(" " * padding + output)

                    if len(inp.split(".")) > 1:
                        module_com = inp.split(".")
                        module = module_com[1]                            

                       if len(module_com) == 2:
                            if module in shell.env['scripts']:                            
                                for script_var in shell.env['script_vars'][module]:
                                    print(" " * padding + "%s: %s" % (script_var, shell.env['script_vars'][module][script_var]))

                        if len(module_com) == 3:
                            module_var = module_com[2].split(" = ")[0]

                            if inp.find("=") != -1:
                                var_value = inp.split(" = ")[1]
                                shell.curr_com = make_json(
                                    query_type='script_action',
                                    action='set_var',
                                    entity=module,
                                    target=module_var,
                                    var_value=var_value,
                                )
                                
                                host_resp = None

                if shell.curr_com != None:
                    curr_com = json.dumps(shell.curr_com).encode()

                    try:
                        shell.host_socket.sendall(curr_com)
                    except Exception as e:
                        print(e)
                        print("Could not send command to host")

            except KeyboardInterrupt:
                print("\nCTRL+C was used; shell interrupted.")
                break