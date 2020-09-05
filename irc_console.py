commandfile = "command_temp.txt"
configfile = "env.txt"
shellname = "MyBot"

class IRCShell:
    def __init__(self):
        self.env = {
            'channels': "",
            'current_channel': "",
        }
        
        self.action = "default"
        self.curr_com = None
        self.curr_chan = None
        self.curr_chan_id = 1




while True:
    #configfile = 
    currentfile = check_command_file(commandfile)

    if shell.action == "default":
        if len(shell.env['channels']) != 0:
            shell.curr_state = " ".join(shell.env['channels']) + "\n"

    try:
        inp = str(input("%s@%s> " % (shellname, shell.curr_chan)))
        
        if inp[0] == "/":   
            com = inp.split(" ")[0]
            msg = " ".join(inp.split(" ")[1:])
            
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

        if shell.curr_com != None:
            with open(commandfile, "w") as c:  
                c.write(shell.curr_com)
            shell.curr_com = shell.curr_state

    except KeyboardInterrupt:
        print("\nCTRL+C was used; shell interrupted.")
        break