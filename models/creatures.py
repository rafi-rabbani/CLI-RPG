from abc import ABC, abstractmethod
from .items import Inventory
import config


class Creature(ABC):
    def __init__(self, name, max_hp, damage):
        self.name = name
        self.max_hp = max_hp
        self.__hp = max_hp
        self.damage = damage

    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod

    @abstractmethod
    def heal_creature(self, amount):
        pass

    @property
    def health(self):
        return self.__hp

    @health.setter
    def health(self, new_hp):
        if new_hp is not None:
            if new_hp >= 0 and new_hp <= self.max_hp:
                self.__hp = new_hp
            elif new_hp < 0:
                self.__hp = 0
            else:
                self.__hp = self.max_hp
        else:
            return False

    def __str__(self):
        if self.health > 0:
            return f"Name\t\t: {self.name.title()}\n\nHP\t\t: ({self.health}/{self.max_hp})\n\nDamage\t\t: {self.damage}"
        else:
            return f"{self.name} is DEAD"


class Player(Creature):
    def __init__(self, name, max_hp, damage):
        super().__init__(name, max_hp, damage)
        self.inventory = Inventory()
        self.current_room = None

    def attack(self, target):
        return target.take_damage(self.damage, self.name)

    def take_damage(self, damage, target):
        if damage >= 0:
            self.health = self.health - damage
            if self.health == 0:
                return f"{self.name} is DEAD"
            else:
    def heal_creature(self, amount):
        if amount:
            self.health += amount
            if self.health > self.max_hp:
                self.health = self.max_hp

    def collect_item(self, item):
        self.inventory.collect_item(item)

    def remove_item(self, item):
        item_list = self.inventory.list_item()
        item_list.remove(item)

    def view_item(self):
        self.inventory.list_item()

    @classmethod
    def fighter(cls, name):
        return cls(name, *list(config.PLAYER["FIGHTER"].values()))

    @classmethod
    def archer(cls, name):
        return cls(name, *list(config.PLAYER["ARCHER"].values()))

    @classmethod
    def tank(cls, name):
        return cls(name, *list(config.PLAYER["TANK"].values()))

    def __str__(self):
        return super().__str__()


class Monster(Creature):
    def __init__(self, name, max_hp, damage):
        super().__init__(name, max_hp, damage)

    def attack(self, target):
        return target.take_damage(self.damage, self.name)

    def take_damage(self, damage, target):
        if damage >= 0:
            self.health = self.health - damage
            if self.health == 0:
                return f"{self.name} is DEAD"
            else:

    def heal_creature(self, amount):
        if amount:
            self.health += amount
            if self.health > self.max_hp:
                self.health = self.max_hp

    @classmethod
    def dragon(cls):
        return cls(*list(config.MONSTERS["DRAGON"].values()))

    @classmethod
    def goblin(cls):
        return cls(*list(config.MONSTERS["GOBLIN"].values()))

    @classmethod
    def skeleton(cls):
        return cls(*list(config.MONSTERS["SKELETON"].values()))

    @classmethod
    def minotaur(cls):
        return cls(*list(config.MONSTERS["MINOTAUR"].values()))

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f"{self.name}"
