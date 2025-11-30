class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.monsters = []
        self.exits = {}

    def connects(self, direction, next_room):
        self.exits[direction] = next_room

