from view import ConsoleView
from models import World, Item, Player, Monster
from config import PLAYER

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
        "TURN ORDER\t: The Creature with the LOWEST current HP attacks FIRST in each round.",
        "DEFEAT\t\t: Health (HP) reaching 0 or less results in permanent defeat.",
        "PERSISTENCE\t: Use 'SAVE' to engrave your progress to disk at any time.",
        "EXIT\t\t: Use 'EXIT' or 'QUIT' to stop the game."
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

        orthodox_key    = Item("Orthodox Key"    , f"the key used to open the location of {orthodox.name}")
        ice_key         = Item("Ice Key"         , f"the key used to open the location of {ice.name}")
        unorthodox_key  = Item("Unorthodox Key"  , f"the key used to open the location of {unorthodox.name}")
        demonic_key     = Item("Demonic Key"     , f"the key used to open the location of {demonic.name}")

        cloud.add_item(orthodox_key)
        orthodox.add_item(ice_key)
        ice.add_item(unorthodox_key)
        unorthodox.add_item(demonic_key)

        sword = Item("Worn Iron Sword", "A basic iron sword, showing signs of wear from countless battles. It's a reliable weapon for any adventurer.")
        saber = Item("Jade Green Saber", "A finely crafted saber with a jade green blade, known for its sharpness and elegance.")
        dagger = Item("Frostbone Dagger", "A dagger forged from the bones of ice creatures, it emanates a chilling aura that can freeze anything it touches.")
        greatsword = Item("Bloodthirsty Greatsword", "A massive greatsword that thirsts for the blood of its enemies, radiating a menacing aura.")
        scythe = Item("Demon God's Scythe", "The legendary weapon of the First Heavenly Demon. It radiates an overwhelming aura of dominance. Holding it makes you feel like the absolute ruler of the martial world.")

        cloud.add_item(sword)
        orthodox.add_item(saber)
        ice.add_item(dagger)
        unorthodox.add_item(greatsword)
        demonic.add_item(scythe)

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
        last_message = ''
        command = ''

        while self.is_running:
            if command == 'exit':
                break

            self.view.show_game_screen(command, last_message, self.player)
            command = self.view.get_player_command()
            
            last_message = self.process_command(command)


    def process_command(self, command):
        word = command.split()
        action = word[0]

        if action == 'menu':
            return self.view.show_menu()

        elif action == 'go':
            if len(command) <= 2:
                return "go where? (north, south, east, west)"
            
            direction = word[1]
            return self.move_player(direction)
        
        elif action == 'inventory':
            return self.view.show_inventory(self.player.inventory)
        
        elif action == 'look':
            return self.view.show_around()
        
        elif action == 'take':
            return self.view.show_take_item(self.player.current_room.items)

        elif action == 'exit':
            return self.view.show_exit_screen(self.player_name)
        
        return 'unknow command'

    def move_player(self, direction):
        current_room = self.player.current_room

        if direction in current_room.exits:
            next_room = current_room.exits[direction]

            opened, item = self.locked_room(direction)

            if opened is True:
                self.player.current_room = next_room
                self.view.show_current_room(next_room)
                return f"you successfully opened location of {next_room.name} using {item.name}"

            elif opened is False:
                return "this location is still locked"

            elif opened is None:
                self.player.current_room = next_room
                self.view.show_current_room(next_room)
                return f"you have moved to {next_room.name}"

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
     
    def locked_room(self, direction):
        current_room = self.player.current_room
        inventory = self.player.inventory

        if direction in current_room.locked_exit:
            key_name = current_room.locked_exit[direction]

            for item in inventory.list_item():
                if key_name == item.name:
                    self.player.remove_item(item)
                    del current_room.locked_exit[direction]

                    return True, item
            return False, None
        return None, None