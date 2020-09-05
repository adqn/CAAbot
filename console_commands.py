import os

class Console:
    def __init__(self):
        self.fileopt =  -2
        self.command_file = "command_temp.txt"
        self.last = os.stat(self.command_file)[self.fileopt]
        self.current_command = None

    def get_command(self):
        try:
            if self.last != os.stat(self.command_file)[self.fileopt]:
                f = open(self.command_file)
                self.current_command = f.readlines()
                self.last = os.stat(self.command_file)[self.fileopt]
                self.status = f.fileno()
                f.close()

                if len(self.current_command) > 1:
                    self.current_command = [c.replace('\n', '') for c in self.current_command]
                else:
                    self.current_command = self.current_command[0]
                
            else:
                self.current_command = None
        except:
            pass
