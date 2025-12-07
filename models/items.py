class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"Name\t\t: {(self.name)}\nDescription\t: {self.description}\n"

    def __repr__(self):
        return f"{self.name}"


class Inventory:
    def __init__(self):
        self.__item_list = []

    def collect_item(self, new_item):
        if isinstance(new_item, Item):
            self.__item_list.append(new_item)
        else:
            return False

    def list_item(self):
        return self.__item_list
