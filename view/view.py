from models import creatures
import os
import time
import shutil
import sys

class ConsoleView:
    def __init__(self):
        self.width_console = shutil.get_terminal_size().columns
        
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def padding_center(self, text):
        padding = (self.width_console - len(text)) / 2
        return int(padding)

    def typing_slow(self, text, speed=0.05, center=True):
        if center:
            sys.stdout.write(" " * self.padding_center(text))

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()
    
    def show_loading_screen(self):
        self.clear_screen()

        print('\n'*16)
        self.typing_slow("W E L C O M E   T O   M U R I M   W O R L D")
        print()
        self.typing_slow('by   F I Z Z')

        time.sleep(0.75)

        print("\n"*4)

        text_enter = 'Press [ENTER] to Start....'
        input(' ' * self.padding_center(text_enter) + text_enter)
        self.clear_screen()

