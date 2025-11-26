from abc import ABC, abstractmethod
from items import Inventory
import config

class Creature(ABC):
    def __init__(self, name, max_hp, damage):
        self.name = name
        self.max_hp = max_hp
        self.__hp = max_hp
        self.damage = damage

    @abstractmethod
    def attack():
        pass

    @abstractmethod
    def defend():
        pass

    @property
    def health(self):
        return self.__hp
    
    @health.setter
    def health(self, new_hp):
        if new_hp:
            if new_hp >= 0 and new_hp <= self.max_hp:
                self.__hp = new_hp
            else:
                print("Invalid HP value")
        else:
            print("Invalid HP value")

    def __str__(self):
        return f"{self.name.upper()}\nHP\t: ({self.health}/{self.max_hp})\nDamage\t: {self.damage}"

class Player(Creature):
    def __init__(self, name):
        super().__init__(name, config.PLAYER["MAX_HP"], config.PLAYER["BASE_DAMAGE"])
        self.inventory = Inventory()

    def attack(self, target):
        print(f"{self.name} attacks {target} with {self.damage} damage")
        target.defend(self.damage)

    def defend(self, damage):
         if damage >= 0:
            new_hp = self.health - damage

            if new_hp < 0:
                self.health = new_hp
                print(f"{self.name} is DIE")
            else:
                print(f"{self.name} takes {damage} damage\nHP\t: ({self.health}/{self.max_hp})")

    def collect_item(self, item):
        self.inventory.add_item(item)
        print("Item added to Inventory")
    
    def view_item(self):
        self.inventory.list_item()

