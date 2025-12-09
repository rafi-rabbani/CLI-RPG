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
        return int((self.width_console - len(text)) / 2)

    def space_text(self, text):
        return " ".join(text)

    def wait(self, time_sleep=1):
        time.sleep(time_sleep)

    def typing_slow(self, text, speed=0.03, center=True):
        if center:
            sys.stdout.write(" " * self.padding_center(text))

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            self.wait(speed)
        print()

    def wait_for_enter(self, text_enter, enter_line, time_sleep=1):
        self.wait(time_sleep)

        print("\n" * enter_line)
        input(" " * self.padding_center(text_enter) + text_enter)

    def show_welcome_screen(self):
        self.clear_screen()

        print("\n" * 17)
        self.typing_slow(self.space_text("welcome to").upper())
        print("\n")
        self.typing_slow(self.space_text("the world of murim").upper())
        print("\n")
        self.typing_slow("by  Fizz")

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 14)

    def get_player_name(self):
        self.clear_screen()

        print("\n" * 20)
        self.typing_slow(self.space_text("enter your name").upper())
        print("\n" * 2)

        player_name = input(" " * self.padding_center("sora tansaro") + "")

        print("\n" * 13)

        return player_name if player_name.strip() != "" else "Nameless Wanderer"

    def get_player_role(self, roles):
        role = ""

        while True:
            if role.strip() in ["1", "2", "3"]:
                return list(roles)[(int(role)) - 1].lower()
            else:
                self.clear_screen()

                print("\n" * 15)
                self.typing_slow(self.space_text("choose your destiny").upper())
                print("\n" * 2)

                for role in roles:
                    self.typing_slow(
                        f">>>           {self.space_text(role)}           <<<".upper(),
                        0.01,
                    )
                    print("\n")

                print("\n" * 2)
                print(" " * self.padding_center("( 1 - 3 )") + "( 1 - 3 )\n")

                self.wait(1)

                role = input(" " * self.padding_center(" ") + "")

    def show_rules(self, rules):
        self.clear_screen()

        print("\n" * 8)
        self.typing_slow(self.space_text("the rules").upper())
        print()
        self.typing_slow(self.space_text("of the world of murim").upper())
        print("\n" * 3)

        for index, rule in enumerate(rules):
            print(" " * 36, end="")
            self.typing_slow(f"{index+1}. {rule}\n", 0.01, False)

        text_enter = "Press [ENTER] to Next...."
        self.wait_for_enter(text_enter, 13)

    def show_start_screen(self, name):
        self.clear_screen()

        print("\n" * 20)
        self.typing_slow(self.space_text(name).upper())
        print()
        self.typing_slow(self.space_text("your journey starts here").upper())

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 15)

    def show_current_room(self, room):
        self.clear_screen()

        print("\n" * 16)
        self.typing_slow(self.space_text(f"location:").upper())
        print("\n\n")
        self.typing_slow(self.space_text(f"{room.name}").upper())
        print()
        self.typing_slow(self.space_text(f"{room.description}").upper())

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 15)

    def show_inventory(self, inventory, status=True):
        if status:
            items = []

            if not inventory.list_item():
                return "empty"

            for item in inventory.list_item():
                items.append(item.name.upper())

            return items
        else:
            return "\n\n".join(str(item) for item in inventory.list_item())

    def show_status_player(self, player):
        print("=" * self.width_console)
        print(" " * self.padding_center("STATUS") + "STATUS")
        print("=" * self.width_console)

        print(player)

        print(f"\nLocation\t: {player.current_room.name}")
        print(f"\nInventory\t: {self.show_inventory(player.inventory)}")
        print()

        print("=" * self.width_console)

    def show_game_screen(self, command, message, player, fight=False):
        self.clear_screen()
        self.show_status_player(player)
        if not fight:
            print("\nNot sure what to do?  'menu' to see what you can do")
        if message != "":
            print(f"\n>>> {command}")
            print(f"\n{message}")

    def show_menu(self):
        return (
            "COMMANDS:\n"
            "- go [direction]  : Move (north, south, east, west)\n"
            "- take [item name]: Pick up an item\n"
            "- use potion      : Use a potion and heal yourself\n"
            "- look            : Inspect the room\n"
            "- inventory       : Check bag\n"
            "- save            : Save game\n"
            "- load            : Load game\n"
            "- exit            : Quit game"
        )

    def get_player_command(self, message=""):
        return input(f"\n>>> {message}").strip().lower()

    def show_message(self, message):
        print(f"\n{message}")

    def show_around(self, room):
        return (
            f"this is {room.name}, {room.description}"
            f"\n\n[items   ] : {room.items}"
            f"\n[exits   ] : [{" ,".join(list(room.exits.keys()))}]"
        )

    def show_exit_screen(self, name):
        self.clear_screen()

        print("\n" * 20)
        self.typing_slow(self.space_text(name).upper())
        print()
        self.typing_slow(self.space_text("you have left the murim world").upper())

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 15)

    def show_monster(self, monster):
        self.clear_screen()

        print("\n" * 20)
        self.typing_slow(self.space_text(f"a wild {monster.name} appears!").upper())
        self.wait(1)

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 17)

    def show_status_combat(self, player, monster, creature, message):
        self.clear_screen()

        message_player = ""
        message_monster = ""

        if creature == "player":
            if message[1] == "+":
                message_player = f"{message}"
            else:
                message_monster = f"{message}"
        elif creature == "monster":
            if message[1] == "+":
                message_monster = f"{message}"
            else:
                message_player = f"{message}"

        print("=" * self.width_console)
        print(" " * self.padding_center("COMBAT MODE") + "COMBAT MODE")
        print("=" * self.width_console)

        name = f"Name   : {player.name.title()}"
        health = f"HP     : ({player.health}/{player.max_hp}) {message_player}"
        damage = f"Damage : {player.damage}"

        monster_name = f"{monster.name.title()} :    Name"
        monster_health = (
            f"{message_monster} ({monster.health}/{monster.max_hp}) :     HP"
        )
        monster_damage = f"{monster.damage} : Damage"

        print()
        print(name, end="")
        print(" " * (self.width_console - (len(name) + len(monster_name))), end="")
        print(monster_name)
        print()
        print(health, end="")
        print(" " * (self.width_console - (len(health) + len(monster_health))), end="")
        print(monster_health)
        print()
        print(damage, end="")
        print(" " * (self.width_console - (len(damage) + len(monster_damage))), end="")
        print(monster_damage)
        print()
        print("=" * self.width_console)

    def show_combat_screen(
        self, player, monster, creature="", message="", message_status=""
    ):
        self.show_status_combat(player, monster, creature, message_status)

        if message != "":
            print()
            self.typing_slow(message, 0.01)

    def show_defeat_screen(self, name):
        self.clear_screen()

        print("\n" * 20)
        self.typing_slow(self.space_text(name).upper())
        print()
        self.typing_slow(self.space_text("you have been slain").upper())

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 15)

    def show_victory_screen(self, name, monster, gift_health, gift_damage):
        self.clear_screen()

        print("\n" * 18)
        self.typing_slow(self.space_text(name).upper())
        print()
        self.typing_slow(
            self.space_text(f"you successfully defeated the {monster.name}").upper()
        )
        print("\n")
        self.typing_slow(self.space_text(f"[MAX HP: {gift_health}++]"))
        print()
        self.typing_slow(self.space_text(f"[DAMAGE: {gift_damage}++]"))

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 12)

    def show_end_game(self, name):
        self.clear_screen()

        print("\n" * 20)
        self.typing_slow(self.space_text(f"[congratulation {name}!!!]").upper())
        print()
        self.typing_slow(
            self.space_text(
                "you have successfully conquered the world of Murim"
            ).upper()
        )
        print()
        self.typing_slow(
            self.space_text("now you are the ruler of the entire land of Murim").upper()
        )

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 13)
        
    def show_load_screen(self, name):
        self.clear_screen()
        
        print("\n" * 20)
        self.typing_slow(self.space_text(name).upper())
        print()
        self.typing_slow(self.space_text("welcome back in the world of murim").upper())

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 15)
        
    def show_error_screen(self, message):
        self.clear_screen()
        
        print("\n" * 20)
        self.typing_slow(self.space_text(message).upper())

        text_enter = "Press [ENTER] to Start...."
        self.wait_for_enter(text_enter, 17)
