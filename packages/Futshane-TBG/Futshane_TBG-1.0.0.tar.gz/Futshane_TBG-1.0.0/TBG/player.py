# This contains the classes for creating interactive beings

from random import randint as random
from typewriter import typewriter    # Substitute of the "print" function


def cleaner(f):     # Wrapper function
    """Make printed text easier to read by creating borders around text"""

    def wrap(*args, **kwargs):
        print("==" * 20)
        f(*args, **kwargs)
        print("==" * 20)
        print("\n")

    return wrap


class Player:
    """ This is the class for creating the Player of the Game"""

    BAG_CAP = 10  # The maximum capacity of the Player's inventory

    def __init__(self, name, max_hp=100, defence=0):
        self.name = name  # The name of the Player
        self._MAX_HP = max_hp  # The max health of the Player
        self.hp = self._MAX_HP  # The Health of the player
        self.defence = defence  # The defence value
        self._fight_moves = {}  # Dictionary of the players fighting move instances
        self._location = None  # The current room that the player is in, this is a Room class instance
        self._bag = {}  # Dictionary of items that the player has
        self._backstory = "No back story"  # The Player's back story i.e autobiography

    @property
    def bag(self):
        """Returns the dictionary of the items in the players inventory"""
        # The dictionary key to a Item objects is the Item's name attribute
        return self._bag

    @bag.setter
    def bag(self, dicti):
        """Setting the items in the player bag"""
        self._bag = dicti

    @property
    def backstory(self):
        """Returns the text of players back story"""
        return self._backstory

    @backstory.setter
    def backstory(self, txt):
        """Setting the text of backstory"""
        self._backstory = txt

    @property
    def fight_moves(self):
        """"return a dictionary of players fighting moves"""
        # The dictionary key to a fight_move objects is the fight_move's name attribute
        return self._fight_moves

    @fight_moves.setter
    def fight_moves(self, dicti):
        """setting the dictionary of the fight moves """
        self._fight_moves = dicti

    @property
    def location(self):
        """Returns the Room instance of the the players which is the Players current location"""
        return self._location

    @location.setter
    def location(self, room):
        """Setting the current location of the Player"""
        self._location = room

    @cleaner
    def my_story(self):  # Prints the Players back story
        typewriter.typing(self.backstory, 0.035)

    @cleaner
    def take_item(self, obj):
        """ This method allows the Player to remove items from their current location and adds them into their
        inventory """

        """ It will take the dictionary key of the item from the Player's location items attribute,
         then it will remove it from the Room object and add it to Players bag attribute."""

        if obj in self.location.items:  # Testing if "item" key exist in the dictionary

            if obj in self.bag:  # Testing if the "item" key already exist in the Players bag attribute
                typewriter.typing(f"=>{obj} already in bag", 0.035)

            # If the "item" key does'nt exist in the Players bag attribute
            elif len(self.bag) < self.BAG_CAP:  # Testing if Player has reached bag capacity

                self.bag[obj] = self.location.items[
                    obj]  # Appending object to Player's bag attribute, with relevant key
                del self.location.items[obj]  # Removing object from Player's current location

                typewriter.typing(f"=>{obj} is packed in the bag", 0.035)

            else:  # If bag is full
                typewriter.typing(f"=>Bag is full", 0.035)
                typewriter.typing("=>Use the \"throw {item name}\" to make space", 0.035)

        else:  # If the "item" key is not found
            typewriter.typing(f"=>{obj} not in {self.location.name}", 0.035)

    @cleaner
    def search_inv(self):
        """Displays the dictionary of items in Player's bag attribute"""

        if len(self.bag) < 1:  # Testing if there are items to display from the Player's bag attribute
            typewriter.typing(f"=>Bag is empty", 0.035)

        else:  # If the PLayer's bag attribute as items to display

            typewriter.typing(f"=>Items in bag:", 0.035)
            for item in self.bag:
                # Accessing the names of items from the Players bag attribute
                typewriter.typing(f"==>>{item}", 0.035)

    @cleaner
    def examine_item(self, item):
        """ Using 'item' as the key to the item in the Player's bag attribute, it will access that items full_desc
            method """

        if item in self.bag:  # Testing if the key exist

            # Accessing the full description method of the item object
            self.bag[item].full_desc()

        else:  # If the key is not found
            typewriter.typing(f"={item} not in bag", 0.035)

    @cleaner
    def stats(self):
        """ Displays certain Player attributes on the screen"""

        typewriter.typing(f"=>{self.name}'s statistics:", 0.035)

        typewriter.typing(f"==>>Health: {self.hp}", 0.035)  # Displaying Player's current hp value

        typewriter.typing(f"==>>Defence: {self.defence}", 0.035)  # Displaying Player's current defence value

        try:
            typewriter.typing(f"==>>location: {self.location.name}", 0.035)
        except AttributeError:  # If Player is not in a specific room
            pass

        typewriter.typing("\n=>Moves for battle:", 0.035)

        for moves in self.fight_moves:  # Displaying the Player's fighting moves
            typewriter.typing(f"==>>{moves}", 0.035)

    @cleaner
    def throw(self, item):
        """ Uses the 'item' as a key to access the Item object in the Player's bag attribute, the item is removed from
            the bag attribute and is appended into the items dictionary of the Players current location """

        if item in self.bag:  # Testing if key exist

            self.location.items[item] = self.bag[item]  # Appending the item to the items dictionary attribute
            del self.bag[item]  # Removing the item from Players bag attribute
            typewriter.typing(f"=>{item} is thrown away", 0.035)

        else:  # if key doesn't exist
            typewriter.typing(f"=>{item} not in bag", 0.035)

    @cleaner
    def goto(self, new_location):
        """ Ues 'new_location' key to access the location from near_room attribute of Players current location """

        if new_location == self.location.name:  # Testing if Player's location attribute is the same as new_location
            typewriter.typing(f"=>Already in {new_location}", 0.035)

        # testing if new_location is in the near_rooms attribute of Player's location attribute
        elif not (new_location in self.location.near_rooms):

            # If new_location is not in the near_rooms attribute of Player's location
            typewriter.typing(f"=>{new_location} is far from {self.location.name}", 0.035)

        else:  # If new_location is in the near_rooms attribute of Player's location

            self.location = self.location.near_rooms[new_location]  # Changing value of Player's location attribute
            typewriter.typing(f"=>You have entered {new_location}", 0.035)

    @cleaner
    def show_move(self, move):
        """ Using 'move' as the key to the fighting move object in the Player's fighting_moves attribute,
            it will access the fighting_move's full_desc method """

        if not (move in self.fight_moves):  # Testing if key exists
            typewriter.typing(f"=>{self.name} doesnt know this move", 0.035)

        else:  # If key exist

            self.fight_moves[move].full_desc()  # Accessing the full description method of the fight_move object

    @cleaner
    def eat(self, food):
        """ Uses 'food' as key to the Food object in the Players bag attribute """

        if food in self.bag:  # Testing if key exist

            if self.bag[food].type == "Consumable":  # Testing if the item from Player's bag is "Consume" type

                if not (self.hp == self._MAX_HP):  # Test if Player's hp attribute is equal to the MAX_HP attribute
                    self.hp += self.bag[food].regen

                    if self.hp > self._MAX_HP:  # If Players hp attribute exceeds the MAX_HP attribute
                        self.hp = self._MAX_HP

                    typewriter.typing(f"=>Health +{self.bag[food].regen}", 0.085)
                    del self.bag[food]  # Removing the item from Player's bag Attribute

                else:  # If Players hp attribute is equal to the MAX_HP attribute
                    typewriter.typing(f"=>{self.name} is full", 0.035)

            else:  # Item is not "Consumable" type
                typewriter.typing(f"=>{food} is not Consumable type", 0.035)

        else:  # If key does;nt exist
            typewriter.typing(f"=>{food} not in bag", 0.035)

    @cleaner
    def learn(self, scroll):
        """ Uses 'scroll' as key to access the Scroll object from Player's bag attribute and replaces Player's
            fighting_moves dictionary attribute with the Scroll object's fighting_moves"""

        if scroll in self.bag:  # Testing if key exists

            if self.bag[scroll].type == "Learn":  # Testing if item is "Learn" type

                # Replacing Player's fighting move attribute with Scroll objects's fighting move
                self.fight_moves = self.bag[scroll].fight_moves

                typewriter.typing(f"=>{self.name} has learnt the {scroll} scroll", 0.035)
                del self.bag[scroll]  # removing Scroll object from bag

            else:  # If item is not "Learn" type
                typewriter.typing(f"=>{scroll} is not Learn type", 0.035)

        else:  # If key does'nt exist
            typewriter.typing(f"=>{scroll} not in bag", 0.035)

    @cleaner
    def enhance(self, enhancer):
        """ Uses 'enhancer' as key to the Enhancement object in the Player's bag attribute, it will increase the
            damage dealt of specific fight moves from Player's fighting_moves attribute"""

        if enhancer in self.bag:  # Testing if key exist

            if self.bag[enhancer].type == "Improve":  # Testing if item is Improve" type

                executed = False  # Indicates that no fight move has been affected

                for fighting_move in self.fight_moves:  # Increase damage of relevant fighting move(s)

                    # Testing if fight move is the same style as the Enhancer object
                    if self.fight_moves[fighting_move].style == self.bag[enhancer].style:
                        self.fight_moves[fighting_move].damage += self.bag[enhancer].damage
                        executed = True

                # testing if  a move has been improved
                if not executed:
                    typewriter.typing(f"=>No battle move is {self.bag[enhancer].style} style", 0.035)

                else:  # If a fight move has been improved

                    typewriter.typing(f"=>{self.bag[enhancer].style} style fighting moves increased damage by +{self.bag[enhancer].damage}",0.065)
                    del self.bag[enhancer]  # removing the enhancer from bag

            else:  # If item is not "Improve type"
                typewriter.typing(f"=>{enhancer} is not Improve type", 0.035)

        else:  # If key doesn't exist
            typewriter.typing(f"=>{enhancer} not in bag")

    @cleaner
    def equip(self, armor):
        """ Uses 'armor' as key to the Armor object in Player's bag attribute, and replaces the Player's defence
            value with Armor object's defence value"""

        if armor in self.bag:  # Testing if key exist

            if self.bag[armor].type == "Armor":  # Testing if item is "Armor" type

                self.defence = self.bag[armor].defence  # changing players defence value
                typewriter.typing(f"=>{armor} is equipped", 0.085)

                del self.bag[armor]  # removing Armor object from bag

            else:  # If item is not "Armor" type
                typewriter.typing(f"=>{armor} is not Armor type")

        else:  # If key does'nt exist
            typewriter.typing(f"=>{armor} not in bag")

    @cleaner
    def talk(self, npc):
        """ Uses 'npc' as key to access the people attribute of Player's location"""

        if npc in self.location.people:  # Testing key exits

            # Accessing the conversation method of the NPC object in people attribute of Player's location
            self.location.people[npc].conversation()

        else:  # If key doesn't exist
            typewriter.typing(f"=>{npc} is not in the room")

    @cleaner
    def look_around(self):  # Displays useful info about Player's location

        # Printing out the description of the Player's location
        typewriter.typing(self.location.desc, 0.035)

        # Displaying items in Player's location
        if len(self.location.items) < 1:  # Testing if Player's location has Item instances
            typewriter.typing(f"=>{self.location.name} is empty\n")

        else:
            # Display the items in the Player's location
            typewriter.typing(f"\n=>Item to take:")

            # Accessing the items using the dictionary keys from the Player's location items dictionary
            for item in self.location.items:
                typewriter.typing(f"==>>{self.location.items[item].name}", 0.035)
        # =============================

        # Displays the nearby Room exits in Player's location
        if len(self.location.near_rooms) < 1:  # Testing if Player's location has exits to other Room instances

            typewriter.typing(f"\n=>No room nearby")

        else:
            # Display the nearby Room instances
            typewriter.typing(f"\n=>Nearby rooms:")

            # Accessing the rooms using the dictionary keys from the near_room dictionary of Player's location
            for exits in self.location.near_rooms:
                typewriter.typing(f"==>>{self.location.near_rooms[exits].name}", 0.035)
            typewriter.typing("\n")
        # =============================

        # Display the NPC's in the Player's location
        if len(self.location.people) < 1:  # Testing if the Player's location has NPCs

            typewriter.typing(f"\n=>Nobody in room")

        else:

            typewriter.typing(f"=>People to talk to:")

            # Accessing the NPCs using the dictionary keys from the people dictionary
            for person in self.location.people:
                typewriter.typing(f"==>>Name: {self.location.people[person].name}", 0.035)
        # =============================


class NPC:
    """ Class for creating Non Playable Characters(NPC)"""

    def __init__(self, name):
        self._text_opt = ["I have nothing to say"]  # List of different replies of the  NPC
        self.name = name  # Name of NPC

    @property
    def text_opt(self):
        # returns a list of text for conversing
        return self._text_opt

    @text_opt.setter
    def text_opt(self, listi):
        # setting the text_opt with list
        self._text_opt = listi

    def conversation(self):
        """ Select at random a text from the list of the NPC's text_opt attribute and prints it out"""

        selector = random(0, len(self.text_opt) - 1)  # Creating the random selector

        reply = self.text_opt[selector]  # Using the selector to pick text from NPC's text_opt attribute
        typewriter.typing(reply, 0.1)


class Enemy:
    """ Class for creating Enemy objects"""

    def __init__(self, name, hp=100, defence=0):
        self.name = name  # The name of the Enemy
        self.hp = hp  # The Health of the Enemy
        self.defence = defence  # The defence value
        self._fight_moves = {}  # Dictionary of the Enemy's fighting move instances

    @property
    def fight_moves(self):
        """"return a dictionary of Enemy's fighting moves"""
        # The dictionary key to a fight_move objects is the fight_move's name attribute
        return self._fight_moves

    @fight_moves.setter
    def fight_moves(self, dicti):
        """setting the dictionary of the fight moves """
        self._fight_moves = dicti
