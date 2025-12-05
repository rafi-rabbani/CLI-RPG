class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.monsters = []
        self.exits = {}
        self.locked_exit = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def add_monster(self, monster):
        self.monsters.append(monster)

    def connects(self, direction, next_room):
        self.exits[direction] = next_room

    def locked_connects(self, direction, key_name):
        if direction in self.exits:
            self.locked_exit[direction] = key_name

    def __str__(self) : return f"{self.name}"

    def __repr__(self): return self.__str__()

class World:
    def __init__(self):
        self.rooms = {}
        self.starting_room = None
    
    def generate_world(self):
        cloud = Room("Cloud Association", "Association of Players from All Over of The World")
        orthodox = Room("Orthodox Alliance", "The Central Headquarters of Murim Orthodox")
        unorthodox = Room("Unorthodox Alliance", "The Alliance of Unorthodox Murim Martial Artist")
        demonic = Room("Heavenly Demonic Cult", "A Cult Founded by Cheon Ma, The First Heavenly Demon Emperor")
        ice = Room("North Sea Ice Palace", "A palace located in the North Sea whose main attribute is ice")

        orthodox.connects("north", ice)
        orthodox.connects("south", demonic)
        orthodox.connects("west", unorthodox)
        orthodox.connects("east", cloud)

        cloud.connects("west", orthodox)
        unorthodox.connects("east", orthodox)
        demonic.connects("north", orthodox)
        ice.connects("south", orthodox)

        self.rooms = {
            "center" : orthodox,
            "north" : ice,
            "south" : demonic,
            "west" : unorthodox,
            "east" : cloud
        }

        self.starting_room = cloud

