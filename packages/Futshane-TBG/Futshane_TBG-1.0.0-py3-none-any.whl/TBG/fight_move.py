# The module provides the class for creating fighting moves and their essential attributes

from typewriter import typewriter  # Substitute of the "print" function


class Fight:  # Used by player objects to battle each other in the "level" class's battle_loop method

    def __init__(self, name, style="Normal", damage=0):
        self.name = name  # The name of the Fighting move
        self.damage = damage  # The damage inflicted when the move is used
        self._desc = "No description"  # Description of the fighting, like its origins or who made it
        self._atck_desc = ["The attack was painful"]  # The list of descriptive sentences of how the fighting move was used
        self.style = style  # The style of the fighting move eg. Fire or Water or Earth and ect

    @property
    def desc(self):
        # returns the description of the move
        return self._desc

    @desc.setter
    def desc(self, txt):
        # setting the description of the move
        self._desc = txt

    @property
    def atck_desc(self):
        # return a list of descriptive sentences of how the fighting move was used
        return self._atck_desc

    @atck_desc.setter
    def atck_desc(self, listi):
        # setting the descriptive sentences of how the fighting move was used
        self._atck_desc = listi

    def full_desc(self):
        """ This method will print out the useful info about the fight move"""

        # print the description of the move
        typewriter.typing(f"==>{self.name} description: {self.desc}", 0.1)
        # print damage
        typewriter.typing(f"=>Damage: {self.damage}", 0.085)
        # print fighting style
        typewriter.typing(f"=>Style: {self.style} \n", 0.085)
