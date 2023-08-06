# Module for creating items that can be interacted wth in the game
# There are different items to create that have special uses

from typewriter import typewriter   # Substitute of the "print" function


def cleaner(f):     # Wrapper function
    """Makes printed text easier to read by creating borders around text"""

    def wrap(*args, **kwargs):
        print("==" * 20)
        f(*args, **kwargs)
        print(("==" * 20) + "\n")

    return wrap


class Item:
    """ For creating items that have no special use"""

    def __init__(self, name):
        self.name = name  # name of the item
        self._desc = "No description"  # The description of the item
        self.type = "No type"  # Used for determining the use case of the item

    @property
    def desc(self):
        """Return the description of the item"""
        return self._desc

    @desc.setter
    def desc(self, txt):
        """Setting the description of the item"""
        self._desc = txt

    def full_desc(self):
        typewriter.typing(f"==>>{self.name} description: {self.desc}<<== \n", 0.05)


class Food(Item):
    """ For creating items that can increase the Player object's hp attribute"""

    def __init__(self, name, regeneration=0):
        super(Food, self).__init__(name)
        self.regen = regeneration   # The amount of health that the player object will be increased by
        self.type = "Consumable"    # To identify that the object can be consumed

    def full_desc(self):
        """ This method will print out the useful info about the item"""

        # printing object description
        typewriter.typing(f"==>>{self.name} description: {self.desc}<<== \n", 0.035)

        # printing object type
        typewriter.typing(f"=>Type: {self.type}", 0.085)

        # printing regeneration value
        typewriter.typing(f"=>Regeneration: +{self.regen}", 0.085)


class Scroll(Item):

    """ For creating items that contain a dictionary of fighting moves"""

    def __init__(self, name):
        super(Scroll, self).__init__(name)
        self.type = "Learn"  # To identify that this object contains a dictionary of Fight class instances
        self._fight_moves = {}  # The dictionary of instances of Fight class

    @property
    def fight_moves(self):
        """"return a dictionary of instances of the fighting_move class"""
        # The dictionary key to a Fight class instances is it's name attribute
        return self._fight_moves

    @fight_moves.setter
    def fight_moves(self, dicti):
        """setting the dictionary of instances of the fighting_move class"""
        self._fight_moves = dicti

    def full_desc(self):
        """ This method will print out the useful info about the item"""

        # printing object description
        typewriter.typing(f"==>>{self.name} description: {self.desc}", 0.035)

        # printing object type
        typewriter.typing(f"=>Type: {self.type} \n", 0.085)

        # printing the fighting moves
        typewriter.typing(f"=>The {self.name} scroll reads: ")
        for moves in self.fight_moves:
            self.fight_moves[moves].full_desc()


class Enhancement(Item):
    """ For creating items that increase damage value of fighting move"""

    def __init__(self, name, style="Normal", damage_increase=0):
        super(Enhancement, self).__init__(name)
        self.style = style  # for identifying the style of the Fight class instance that it will affect
        self.type = "Improve"   # to identify that the object can be used to improve the Fight class instance's damage attribute
        self.damage = damage_increase  # This attribute is the value of damage that will be used to increase damage.

    def full_desc(self):
        """ This method will print out the useful info about the item"""

        # printing object description
        typewriter.typing(f"==>>{self.name} description: {self.desc}<<== \n", 0.035)

        # printing object type
        typewriter.typing(f"=>Type: {self.type}", 0.085)

        # printing fight style value
        typewriter.typing(f"=>Style target: {self.style}", 0.085)

        # printing damage increase
        typewriter.typing(f"=>Damage: +{self.damage}", 0.085)


class Armor(Item):
    """ For creating items that can change the defence value of a Player object"""

    def __init__(self, name, defence=0):
        super(Armor, self).__init__(name)
        self.defence = defence  # The value that will be used to replace the Player class instance's defence attribute
        self.type = "Armor"     # to identify that the item can be used to change defence value of the Player class instance

    def full_desc(self):
        """ This method will print out the useful info about the item"""

        # printing object description
        typewriter.typing(f"==>>{self.name} description: {self.desc}<<== \n", 0.035)

        # printing object type
        typewriter.typing(f"=>Type: {self.type}", 0.085)

        # printing regeneration value
        typewriter.typing(f"=>Defence: {self.defence}", 0.085)
