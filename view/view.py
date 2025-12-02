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
    
    def space_text(self, text): return " ".join(text)

    def typing_slow(self, text, speed=0.05, center=True):
        if center:
            sys.stdout.write(" " * self.padding_center(text))

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()
    
    def show_welcome_screen(self):
        self.clear_screen()

        print('\n'*17)
        self.typing_slow(self.space_text("welcome to").upper())
        print('\n')
        self.typing_slow(self.space_text("the world of murim").upper())
        print('\n')
        self.typing_slow('by  Fizz')

        time.sleep(1)

        print("\n"*14)

        text_enter = 'Press [ENTER] to Start....'
        input(' ' * self.padding_center(text_enter) + text_enter)

    def show_rules(self, rules):
        self.clear_screen()

        print('\n'*8)
        self.typing_slow(self.space_text("the rules").upper())
        print()
        self.typing_slow(self.space_text("of the world of murim").upper())
        print('\n'*3)
        
        for index, rule in enumerate(rules):
            print(" "*36, end="")
            self.typing_slow(f"{index+1}. {rule}\n", 0.01, False)

        time.sleep(1)
        
        print("\n"*9)

        text_enter = 'Press [ENTER] to Next....'
        input(' ' * self.padding_center(text_enter) + text_enter)
