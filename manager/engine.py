from view import ConsoleView
from models import World, Room
from models import Player
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

    def start_game(self):
        self.world.generate_world()

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

            self.player.current_room = next_room
            # self.view.show_current_room(next_room)
            return f"you have moved to {next_room.name}"
        else:
            return "you can't go that away"
        