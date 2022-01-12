import sys, os, time

class UI():
    total_terminal_msg = 0

    def __init__(self) -> None:
        None
    
    def typewriter_number(self, string : str , color : int, delay : int) -> str:

        colors = ["\033[1;32m", "\033[1;33m", "\033[1;36m", "\033[1;31m"]

        fullstring = "[{0}] {1}".format(self.__class__.total_terminal_msg, string)

        for x in fullstring:
            time.sleep(0.005)
            sys.stdout.write(colors[color] + x)
            sys.stdout.flush()
        
        self.__class__.total_terminal_msg += 1

        time.sleep(delay)

        return ""
    
    def typewriter_text(self, string : str , color : int, delay : int) -> str:
        colors = ["\033[1;32m", "\033[1;33m", "\033[1;36m", "\033[1;31m"]

        for x in string:
            time.sleep(0.005)
            sys.stdout.write(colors[color] + x)
            sys.stdout.flush()

        return ""
