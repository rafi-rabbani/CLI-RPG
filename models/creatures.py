from abc import ABC, abstractmethod

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
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return f"{self.name.upper()}\nHP\t: ({self.health}/{self.max_hp})\nDamage\t: {self.damage}"
