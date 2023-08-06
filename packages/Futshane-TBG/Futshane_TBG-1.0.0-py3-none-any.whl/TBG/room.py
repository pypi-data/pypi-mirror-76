# This module is for creating the rooms that will be a the level
# It will also contain NPC character objects and other instances from Item class


def cleaner(f):     # Wrapper function
    """Makes printed text easier to read by creating border around the text"""

    def wrap(*args, **kwargs):
        print("==" * 20 + "\n")
        f(*args, **kwargs)
        print(("==" * 20) + "\n")

    return wrap


class Room:  # For creating rooms in a Level object

    # The contents of every instances of this class are controlled by the player object

    def __init__(self, name):
        self.name = name  # The name of the room
        self._desc = "No description"  # The description of the room
        self._items = {}  # The dictionary of Item class instance
        self._near_rooms = {}  # The dictionary of related Room class instances
        self._people = {}  # The dictionary of NPC's in the room

    @property
    def desc(self):
        """Return the description of the room"""
        return self._desc

    @desc.setter
    def desc(self, txt):
        """For setting the description  the room"""
        self._desc = txt

    @property
    def items(self):
        """Return a dictionary of item instances in the room"""
        # The dictionary key to a Item is the Item's name attribute
        return self._items

    @items.setter
    def items(self, dicti):
        """for setting the dictionary of item instances in the room"""
        self._items = dicti

    @property
    def near_rooms(self):
        """Return dictionary of Room instances in this Room"""
        # The dictionary key to a Room objects is the Room's name attribute
        return self._near_rooms

    @near_rooms.setter
    def near_rooms(self, dicti):
        """for setting the dictionary of Room instances in this Room"""
        self._near_rooms = dicti

    @property
    def people(self):
        """Return a dictionary of NPC instances"""
        # The dictionary key to a NPC objects is the NPC's name attribute
        return self._people

    @people.setter
    def people(self, dicti):
        """for setting a dictionary of NPC instances"""
        self._people = dicti
