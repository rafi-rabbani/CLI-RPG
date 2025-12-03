class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{(self.name).upper()}\nDeskription\t: {self.description}"

class Inventory:
    def __init__(self):
        self.item_list = []

    def add_item(self, new_item):
        if isinstance(new_item, Item):
            self.item_list.append(new_item)
        else:
            return False

    def list_item(self):
        if self.item_list:
            return self.item_list
        else:
            return False

# fire_sword = item("Fire Sword", "Heaven", "A Sword that can burn a city")
