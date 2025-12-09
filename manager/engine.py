from view import ConsoleView
from models import World, Item, Player, Monster
from config import PLAYER, DB_NAME
import json
import os


class GameEngine:
    def __init__(self):
        self.view = ConsoleView()
        self.world = World()
        self.player = None
        self.is_running = True

    def rules_game(self):
        rules = [
            "OBJECTIVE\t: Explore the Murim World and survive all encounters.",
            "NAVIGATION\t: Use cardinal directions (NORTH, SOUTH, EAST, WEST) to move between locations.",
            "STATE CHANGE\t: Encountering a monster immediately initiates COMBAT mode.",
            "DEFEAT\t\t: Health (HP) reaching 0 or less results in permanent defeat.",
            "PERSISTENCE\t: Use 'SAVE' to engrave your progress to disk at any time.",
            "EXIT\t\t: Use 'EXIT' to stop the game.",
        ]
        return rules
 
    def roles(self):
        role = PLAYER.keys()
        return role

    def populate_world(self):
        cloud = self.world.starting_room
        orthodox = self.world.rooms["center"]
        ice = self.world.rooms["north"]
        unorthodox = self.world.rooms["west"]
        demonic = self.world.rooms["south"]

        goblin = Monster.goblin()
        skeleton = Monster.skeleton()
        minotaur = Monster.minotaur()
        dragon = Monster.dragon()

        orthodox.add_monster(goblin)
        ice.add_monster(skeleton)
        unorthodox.add_monster(minotaur)
        demonic.add_monster(dragon)

        orthodox_key = Item(
            "Orthodox Key", f"the key used to open the location of {orthodox.name}"
        )
        ice_key = Item("Ice Key", f"the key used to open the location of {ice.name}")
        unorthodox_key = Item(
            "Unorthodox Key", f"the key used to open the location of {unorthodox.name}"
        )
        demonic_key = Item(
            "Demonic Key", f"the key used to open the location of {demonic.name}"
        )

        cloud.add_item(orthodox_key)
        orthodox.add_item(ice_key)
        ice.add_item(unorthodox_key)
        unorthodox.add_item(demonic_key)

        potion = Item("Potion", "A God-Given Liquid that Can Provide Full Regeneration")

        orthodox.add_item(potion)
        ice.add_item(potion)
        unorthodox.add_item(potion)
        demonic.add_item(potion)

        cloud.locked_connects("west", orthodox_key.name)
        orthodox.locked_connects("north", ice_key.name)
        orthodox.locked_connects("west", unorthodox_key.name)
        orthodox.locked_connects("south", demonic_key.name)

    def start_game(self):
        self.world.generate_world()
        self.populate_world()

        self.view.show_welcome_screen()

        self.player_name = self.view.get_player_name()
        self.player_role = self.view.get_player_role(self.roles())

        self.view.show_rules(self.rules_game())
        self.view.show_start_screen(self.player_name)
        self.view.show_current_room(self.world.starting_room)

        match self.player_role:
            case "fighter":
                self.player = Player.fighter(self.player_name)
            case "archer":
                self.player = Player.archer(self.player_name)
            case "tank":
                self.player = Player.tank(self.player_name)

        self.player.current_room = self.world.starting_room

        self.loop_game()

    def loop_game(self):
        last_message = ""
        command = ""

        while self.is_running:
            if command == "exit":
                break
            elif last_message == "defeat":
                break
            elif last_message == "end":
                self.view.show_end_game(self.player_name)
                break

            self.view.show_game_screen(command, last_message, self.player)
            command = self.view.get_player_command()

            last_message = self.process_command(command)

    def process_command(self, command):
        try:
            word = command.split()
            action = word[0]

            if action == "menu":
                return self.view.show_menu()

            elif action == "go":
                return (
                    "go where? (north, south, east, west)"
                    if len(command) <= 2
                    else self.move_player(word[1])
                )

            elif action == "take":
                return (
                    "take what? (item name)"
                    if len(command) <= 4
                    else self.take_item(" ".join(word[1:]))
                )
            
            elif action == "use":
                if len(command) <= 3:
                    return "use what? (potion)"

                elif word[1] == "potion":
                    heal = self.heal_player()

                    return "you have used a potion and your health has been fully restored" if heal else "you don't have a potion"

            elif action == "look":
                return self.view.show_around(self.player.current_room)

            elif action == "inventory":
                return self.view.show_inventory(self.player.inventory, False)

            elif action == "exit":
                self.save_game()
                return self.view.show_exit_screen(self.player.name)

            else:
                return "unknown command"
        
        except IndexError:
            return "unknown command"

    def move_player(self, direction):
        current_room = self.player.current_room
        previous_room = current_room
        message = ""

        if direction in current_room.exits:
            next_room = current_room.exits[direction]

            opened = self.locked_room(direction)

            if opened is False:
                return "this location is still locked"

            self.player.current_room = next_room
            self.view.show_current_room(next_room)

            if next_room.monsters:
                fight = self.start_fight()

                if fight == "flee":
                    self.player.current_room = previous_room
                    self.view.show_current_room(previous_room)
                    return f"you returned to {previous_room.name}"

                elif fight == "victory":
                    message = " and defeated the monster"

                elif fight == "defeat":
                    return "defeat"
                
                elif fight == "end":
                    return "end"

            if opened is True:
                return f"you successfully opened location of {next_room.name}{message}"

            elif opened is None:
                return f"you have moved to {next_room.name}{message}"

        else:
            return "you can't go that away"

    def take_item(self, item_name):
        current_room = self.player.current_room

        for item in current_room.items:
            if item.name.lower() == item_name:
                self.player.collect_item(item)
                current_room.remove_item(item)
                return f"item {item.name.title()} was successfully saved in inventory"

        return "item not found"

    def heal_player(self):
        inventory = self.player.inventory
        for item in inventory.list_item():
            if item.name.lower() == "potion":
                self.player.heal_creature(self.player.max_hp)
                self.player.remove_item(item)
                return True
        return False

    def locked_room(self, direction):
        current_room = self.player.current_room
        inventory = self.player.inventory

        if direction in current_room.locked_exit:
            key_name = current_room.locked_exit[direction]

            for item in inventory.list_item():
                if key_name == item.name:
                    self.player.remove_item(item)
                    del current_room.locked_exit[direction]

                    return True
            return False
        return None

    def start_fight(self):
        current_room = self.player.current_room
        monster = current_room.monsters[0]

        self.view.show_monster(monster)

        while True:
            self.view.show_combat_screen(self.player, monster)
            question = "[fight/flee]: "
            command = self.view.get_player_command(question)

            if command == "fight":
                return self.loop_fight(monster)
            elif command == "flee":
                return "flee"

    def loop_fight(self, monster):
        is_fighting = True
        player = self.player
        current_room = self.player.current_room

        while is_fighting:
            message, message_status = player.attack(monster)
            
            self.view.show_combat_screen(player, monster, "player", message, message_status)

            self.view.wait(2)

            if monster.health <= 0:
                if monster.name == "DRAGON":
                    return "end"
                gift_health, gift_damage = self.gift_monster(monster)
                self.view.show_victory_screen(self.player_name, monster, gift_health, gift_damage)
                del current_room.monsters[0]
                return "victory"

            if player.health < player.max_hp * (20 / 100):
                while True:
                    self.view.show_message("your health power is less than 20%")
                    question = "[fight/flee]: "
                    command = self.view.get_player_command(question)
                    if command == "flee":
                        return "flee"
                    elif command != "fight":
                        continue

            message, message_status = monster.act(player)
            self.view.show_combat_screen(player, monster, "monster", message, message_status)

            self.view.wait(2)

            if player.health <= 0:
                self.view.show_defeat_screen(self.player_name)
                return "defeat"
            
    def gift_monster(self, monster):
        gift_health, gift_damage = self.player.level_up(monster)

        return gift_health, gift_damage

    def save_game(self):
        data = {
            "player" : self.player.to_dict(),
            "world_rooms" : {}
        }

        for key, room in self.world.rooms.items():
            data["world_rooms"][key] = room.to_dict()

        try:
            with open(DB_NAME, "w") as file:
                json.dump(data, file, indent=4)
                return "[game successfully saved]"
        except:
            return "[error saving game]"

