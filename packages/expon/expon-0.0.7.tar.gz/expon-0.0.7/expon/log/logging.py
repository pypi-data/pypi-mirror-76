import sys
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout, mode='w'):
        self.terminal = stream
        self.log = open(filename, mode)
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass
   

def terminal_to_log(log_filepath):
    sys.stdout = Logger(log_filepath, sys.stdout)
    sys.stderr = Logger(log_filepath, sys.stderr, mode='a')
    # sys.stderr = Logger('a.log_file', sys.stderr)