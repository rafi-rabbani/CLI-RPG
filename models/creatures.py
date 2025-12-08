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

    def level_up(self, monster):
        gift_health = config.MONSTERS[monster.name.upper()]["GIFT_HEALTH"]
        gift_damage = config.MONSTERS[monster.name.upper()]["GIFT_DAMAGE"]

        self.max_hp += gift_health
        self.damage += gift_damage

        return gift_health, gift_damage

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
        self.heal = True
        self.berserk = True

    def act(self, target):
        monster = config.MONSTERS[self.name.upper()]

        if self.health < self.max_hp * (20 / 100) and self.heal:
            heal = int(self.max_hp * monster["HEAL"])
            self.heal_creature(heal)
            self.heal = False
            return f"{self.name} healed himself", f"(+{heal})"

        elif target.health < target.max_hp * (30 / 100) and self.berserk:
            damage = int(self.damage * monster["BERSERK"])
            self.berserk = False
            return self.berserk_attack(target, damage)

        else:
            return self.attack(target)

    def attack(self, target):
        return target.take_damage(self.damage, self.name)

    def berserk_attack(self, target, damage):
        message = target.take_damage(damage, self.name)
        return f"CRITICAL HIT!! {message[0]}", f"(-{damage})"

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
