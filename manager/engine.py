from view.view import ConsoleView
from models.world import World

class GameEngine:
    def __init__(self):
        self.view = ConsoleView()
        self.world = World()

    def start_game(self):
        self.world.generate_world()

        self.view.show_loading_screen()

            
            
            
        