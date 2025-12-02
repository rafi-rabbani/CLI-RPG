from view import ConsoleView
from models import World
from models import Player
from config import PLAYER

class GameEngine:
    def __init__(self):
        self.view = ConsoleView()
        self.world = World()

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

    def start_game(self):
        self.world.generate_world()

        self.view.show_welcome_screen()

        self.player_name = self.view.get_player_name()

        self.view.show_rules(self.rules_game())



            
            
            
        