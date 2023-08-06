
# Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Scope of functionality](#Scope-of-functionality)

#  Introduction

This package provides tools for creating simple Text Based Games while still satisfying players reading needs.

It allows book writers to create an interactive games of literature.
The tools allow player/readers to explore the worlds from the book and interact with items, people and even have battles with antagonists
of the book.

 >This package was initially designed for RPG and  Adventure games
 but it is not limited to these genres.


# Technologies

pygame is only used for playing background music, hopefully future updates do not affect the music functionality but the package is not necessarily required.

The typewriter module is also in use, its use case is for printing individual characters at a specific speed.

The package is developed in pure Python3.8


# Scope of functionality

The package provides multiple tools that make it easy to start developing a simple Text Based Game.

Your project folder should include the following modules:
-   [CMD.py](#Module:-CMD)
-   [level.py](#Module:-level)
-   [player.py](#Module:-player)
-   [fight_move.py](#Module:-fight_move)
-   [room.py](#Module:-room)
-   [item.py](#Module:-item)

# Module: CMD

This module contains the Cmd class.
The  module allows you to detect multiple synonyms for an action/verb

**Class:** Cmd

      def __init__(self, name):
         self._command_list = []
         self.name = name

-   On initialization the CMD instance needs a name, its name attribute will be used as the main word of the group of synonyms.

*   Available option include:
    *   "eat": Command for eating 
    *   "ex_help": command for displaying help text for explore environment **(The package has default help text, called 
    "default_help.py" inside the script load in 'def_ex_help')**
    *   "goto":  command fro changing location
    *   "look_around": command for examining the room
    *   "examine_item": command fro examining items
    *   "throw": command for disposing items from inventory
    *   "talk": command for conversing with NPC objects
    *   "take_item": command for taking items from room
    *   "search_inv": command for displaying items that in inventory
    *   "stats": command for displaying players statistics
    *   "my_story": command for displaying player backstory
    *   "show_move": command for displaying statistics of a Fight class instance
    *   "learn": command for learning new fighting moves
    *   "enhance": command for using an object to increase damage of a fight move
    *   "equip": command for equipping armor
    *   "battle_help": command for displaying help text for battle environment **(The package has default help text, called 
    "default_help.py" inside the script load in 'def_bat_help')**
    *   "attack": command for using a fight move against an opponent  
    *   "proceed": command to exit the exploration loop   


          # Example use
          from TBG.CMD import Cmd

          eat = Cmd("eat")
          print(eat.name)
          >>'eat'

-   Now we need to provide the object with a list of synonyms
related to the name.

-   eg. Lets say the player wants to consume a food item, we have a method
that takes care of that process. Our game has multiple functionality we need a way to identify the specific action/verb, also our method needs
an argument to identify the food item.

-  To extract the information we will make us of the 're module'
it will detect the related synonyms and the argument required

*    your patter must follow this format:   

>   "(synonyms)(\s*)(?P\<arg1>\[word extractor]*)(\s*)"


          # Example use
          ...
          synonym1 = r"(consume)(\s*)(?P<arg1>[\w\']*)(\s*)"
          synonym2 = r"(chow)(\s*)(?P<arg1>[\w\']*)(\s*)"

          eat.command_list = [synonym1, synonym2]

What we did here is create our pattern that will capture the
word "consume" or "chow" which are both words related to eating something. Followed by an optional white space character
, lastly the argument which will be passed in to the method. 

>Always name the argument 'arg1'

> You have the option of having all the synonyms in one pattern, but it will have a lot of clutter

       # Example use

       synonym = r"([(chow)(consume)])(\s*)(?P<html>[\w\']*)"

       eat.command_list = [synonym]


-   After creating your pattern list you will be able to use the 'breaker' method. The method takes in the
players input and test if their command is related to a specific Cmd object. It will return False if it doesnt find a match and if it
does it will return an re.match object.

**Method:** breaker(self)

      # Example use

      player_input1 = "consume Pizza"
      player_input2 = "fight villian"

      eat.breaker(player_input1)
      >> re.match object; span(0, 13), match="consume Pizza"

      eat.breaker(player_input2)
      >>False

from the re.match object we can extract our argument value

       # Example use

       match = eat.breaker(player_input1)

       print(match.group("arg1"))
       >>Pizza

# Module: fight_move

The module provides the class for
creating fighting moves with their essential attributes

Used by the Player class instance and the Enemy class instance to
battle each other

**Class:** Fight

     def __init__(self, name, style="Normal", damage=0):
         self.name = name
         self.damage = damage
         self._desc = "None"
         self._atck_desc = []
         self.style = style

*  **self.name**: Used to identify the fight move
*  **self.damage**: Value used to subtract from opponent's hp attribute

*  **self._desc**:  Description of the fight move. This attribute has
a property method for changing its value, the name of the property is  similar to the name of the particular attribute excluding the underscore

*  **self.style**: Used to specify the style of the fight move, default is "Normal

         # Example use

         from TBG.fight_move import Fight

         kick = Fight("Kick", style="Normal", damage="50")
         kick.desc = "Normal human kick"

*  **self._atck_desc**: The list of descriptive sentences of how the fight move was used, has a property method for setting the list.
The name of the property method is similar to the attribute name excluding the underscore

          ...
          # Example use

          list = ["Very hard blow on the oponent's head", "slide kick on the legs", "Deadly kick on the chest, rndering the oponent breath less"]
          kick.atck_desc = list
          ...


# Module: item

Contains classes for creating objects with unique uses.

*   [**Food**](#**Class:**-Food(item)): Increases Player class instance's hp attribute
*   [**Scroll**](#**Class:**-Scroll(item)): Changing Player class instance's fight_moves dictionary of Fight class instances
*   [**Enhancement**](#**Class:**-Enhancement(item)): Increase damage attribute for Player class instance's fight moves
*   [**Armor**](#**Class:**-Armor(item)):  Changing Player class instance's defence attribute


### **Class:** Item

Has no special use in th game, contains the basic attribute of an item of the game.

     def __init__(self, name):
        self.name = name
        self._desc = "None" 
        self.type = "None"  

*   All object will inherit the following values:
    *   **self.name**:   name of the item
    *   **self._desc**: The description of the item, has
    a property method for changing its value, the name of the property is  similar to the name of the particular 
    attribute excluding the underscore
    *   **self.type**: Used for determining the use case of the item **Shouldn't be changed**


    # Example use

    from TBG.item import Item

    stone = Item("Stone")
    stone.desc = "Stone amomgst a group of stone on the floor"

### **Class:** Food(Item)

    def __init__(self, name, regeneration=0):
       super(Food, self).__init__(name)
       self.regen = regeneration
       self.type = "Consumable"

The Food class inherits from Item class and has the basic attributes of an item.

*   **self.regen**: Value used to increase Player class instance's hp attribute
*   **self.type**: To identify that the object can be consumed. **Shouldn't be changed**

        # Example use 
        
        from TBG.item import Food
        
        pizza = Food("Pizza", regeneration=50)

**Method**: full_desc(self)

Takes no positional arguments.

This method will print out the useful info about the Food instances.

>  The typewriter module is used here to print the individual characters at a specific speed

### **Class:** Scroll(Item)

The Scroll class inherits from Item class the basic attributes of an item.

    def __init__(self, name):
       super(Scroll, self).__init__(name)
       self.type = "Learn"
       self._fight_moves = {}

*   **self.type**: To identify that this object contains a dictionary of Fight class instances. **Shouldn't be changed**
*   **self._fight_moves**: The dictionary of Fight class instances, has
a property method for changing its value, the name of the property is  similar to the name of the particular attribute excluding the underscore


     # Example use

     from TBG.item import Scroll
     from TBG.fight_move import Fight

     Dragon_book = Scroll("Dragon_book")
     Dragon_book.desc = "This scroll will teach you the moves of the amazing kunfu master, Dragon bokie."

     # Our dictionary of Fight class instances
     punch = Fight("punch", damage=10)

     dict =  {punch.name: punch}

     Dragon_book.fight_moves = dict

**Method:** full_desc(self)

Take no positional arguments

Prints out the Scroll class instance's description and displays the attributes of it's dictionary of Fight class instances

>  The typewriter module is used here to print the individual characters at a specific speed

### **Class:** Enhancement(Item)

The Enhancement class inherits from Item class the basic attributes of an item.

Used to increase the damage attribute of specific Fight class instances

    def __init__(self, name, style, damage_increase=0):
       super(Enhancement, self).__init__(name, damage_increase)
       self.style = style
       self.type = "Improve"

*   **self.style**: For identifying the style of the Fight class instance that it will affect
*   **self.type**: to identify that the object can be used to improve the Fight class instance's damage attribute **Shouldn't be changed**
*   **self.damage**: damage_increase: This attribute is the value of damage that a specific
Fight class instance's damage attribute will be increased by.

         # Example use

         from TBG.item import Enhancement

         dumbbell = Enhancement("dumbbell", style="Normal", damage_increase=5)
         dumbbell.desc = "rusty but still does the job"

**Method:** full_desc(self)

Takes no positional arguments

Displays the instances name, damage and style attributes

    # Example use
    ...
    dumbbell.full_desc()
    ...

> The typewriter module is used here to print the individual characters at a specific speed

### **Class:** Armor(Item)

The Armor class inherits from Item class the basic attributes of an item.

Instances of this class are used to replace the defence attribute of Player class instance

       def __init__(self, name, defence=0):
           super(Armor, self).__init__(name)
           self.defence = defence
           self.type = "Armor" to identify that the item can be used to change defence value o the player

*  **self.defence**: The value that will be used to replace the Player class instance's defence attribute
*  **self.type**: To identify that the item can be used to change defence value of the player class instance

        # Example use

        from TBG.item import Armor

        chestplate = Armor("chestplate", 10)
        chestplate.desc = "Normal peace of armor"

**Method:** full_desc(self)

Takes no positional arguments

Displays the instances description and defence attribute

    # Example use

    chestplate.full_desc()

>  The typewriter module is used here to print the individual characters at a specific speed

# Module: room

The room module contains the Room class.

The class is used to create different environments that can be explored by Player class instance.

> The class is not restricted for making closed rooms, it is designed to fit any type of setting outdoor and indoor.

### Class: Room

     def __init__(self, name):
        self.name = name
        self._desc = "None"  # The description of the room
        self._items = {}  # The dictionary of Item class instance
        self._near_rooms = {}  # The dictionary of related Room class instances
        self._people = {}  # The dictionary of NPC's in the room
        
*   **self.name**: The name of the room 
*   **self._desc**: The description of the Room instance
*   **self._items**: This is a dictionary of item class instances.
 It has a property method for setting its values 
 *  **self._near_room**: The dictionary of related Room instances. It has a property method for setting its values 
 *  **self._people**: This is the dictionary of instances of NPC class from the player module
 
        # Example use 
        
        from TBG.item import Food
        from TBG.item import Armor
        from TBG.player import NPC
        from TBG.room import Room
        
        # main room
        bedroom = Room("My_room")
        
        #item for the main room
        shirt =  Armor("T-shirt", 2)
        soda = Food("Soda")
        
        # Related rooms
        bathroom =  Room("bathroom")
        kitchen = Room("kitchen")
        
        # connecting rooms
        kitchen.near_rooms = {bathroom.name: bathroom, bedroom.name: bedroom}
        bedroom.near_rooms = {bathroom.name: bathroom, kitchen.name: kitchen}
        bathroom.near_rooms = {bedroom.name: bedroom, kitchen.name: kitchen}
        
        # NPC's
        mum = NPC("Mum")
        dad = NPC("Dad")
        
        bedroom.items = {shirt.name: shirt, soda.name: soda}
        bedroom.people = {mum.name: mum, dad.name: dad}
  
>   Just remember that since the _near_rooms attribute contains instances of Room class, those rooms also require item,
 NPC, and Room instances 
     
# Module: player

This module contains the classes for creating characters that can be interacted with.

*   Enemy class
*   NPC class
*   Player class
  

### Class: NPC

This class is used for creating non-playable characters

They don't have special functionality other saying random text.

     def __init__(self, name):
        self._text_opt = [] 
        self.name = name 

*   **self.name**:           Name of NPC
*   **self.text_opt**:       List of different replies of the  NPC, It has a property method for setting its values 

        # Example use
        
        from TBG.player import NPC
    
        Mum = NPC("Mum")
        Dad = NPC("Dad")
    
        # List of replies
        Mum_reply = ["Hello Dear, hows your day going so far", "I hope your room is clean, I'm coming to check as soon as I'm lifting these weights"]
        Dad_reply = ["Hay son wanna go play some games", "I juts wanna go sleep ,YAAAAAWN."]
    
        Mum.text_opt = Mum_reply
        Dad.text_opt = Dad_reply
        
    
### Class: Enemy

This class is used to make enemies that will battle with Player class instances

     def __init__(self, name, hp=100, defence=0):
        self.name = name
        self.hp = hp
        self.defence = defence 
        self._fight_moves = {}  
                    
*   **self.name**: The name of the Enemy instance
*   **self.hp**:   The Health of the Enemy instance
*   **self.defence**: The value that an attack damage will be reduced by
*   **self._fight_moves**:  Dictionary of Fight class instances, It has a property method for setting its values 

        # Example use
        
        from TBG.player import Enemy
        from TBG.fight_move import Fight
        
        Loki = Enemy("Loki", defence=1000)
        
        # Fight class instances
        
        Slap = Fight("Slap", damage=10)
        headbutt = Fight("Headbutt", damage=100)
        
        Loki.fight_moves = {Slap.name: Slap, headbutt.name: headbutt}


### Class: Player

The Player class is used to make gama characters/main character of the story.

Instances of this class have thr ability to interact with their environment and make use of the class instances and change their attribute value

    BAG_CAP = 10  

    def __init__(self, name, max_hp=100, defence=0):
        self.name = name  
        self._MAX_HP = max_hp
        self.hp = self._MAX_HP 
        self.defence = defence 
        self._fight_moves = {} 
        self._location = None 
        self._bag = {}  
        self._backstory = "None"  

*   **BAG_CAP**: The maximum capacity of the Player's bag attribute
*   **self.name**: The name of the Player instances
*   **self._MAX_HP**: The max hp value
*   **self.hp**:  The Health of the player
*   **self.defence**:  The value that an attack damage will be reduced by
*   **self._fight_moves**: Dictionary of Fight class instances,  It has a property method for setting its values 
*   **self._location**: This attribute is used to identify the room that the Player instance is in, the value is a Room class Instance
*   **self._bag**: Dictionary of instances from item module
*   **self._backstory**: The Player instance's back story i.e autobiography

        # Example use
        
        from TBG.player import Player
        
        James = Player("James", max_hp=50, defence=100)

**Method:** take_item(self, item)

*   The functions controls the act of removing an item instance from a Room instance's items dictionary.

*   The argument 'item' is the key to the dictionary of items in the Player instance's current location.

*   The function uses the location attribute to identify the current Room the Player instance is an removes the item from the items attribute and appends is to Player instances bad attribute

        # Example use
        
        from TBG.player import Player 
        from TBG.room import Room
        from TBG.item import Food
        
        # Room instance
        Bedroom =  Room("Bedroom")
        
        # Food instance
        Pizza = Food("Pizza", regeneration=10)
        
        # adding item to the room
        Bedroom.items = {Pizza.name:Pizza}
        
        # connecting rooms
        kitchen.near_rooms = {bathroom.name: bathroom, Bedroom.name: Bedroom}
        Bedroom.near_rooms = {bathroom.name: bathroom, kitchen.name: kitchen}
        bathroom.near_rooms = {Bedroom.name: Bedroom, kitchen.name: kitchen}
        
        # setting players location
        James.location = Bedroom
        
        # take_item
        James.take_item("Pizza")

**Method:** search_inv(self)

*   The function controls the act of displaying the item Player instances bag attribute.

*   The function will iterate through all the item instances of the Player instance bag attribute.
    
        # Example use
        ...
        James.search_inv()
        ...

**Method:** def examine_item(self, item)

*   The function calls the full_desc() method of instances from item module

*   The argument 'item' is used as the key for finding the item instance in the Player instances bag attribute.

        # Example use
         ...
        James.examine_item("Pizza")
         ...
     
**Method:** my_story(self)

*   This attribute displays the Player instance's backstory attribute.

        # Example use 
        ...
        James.backstory = "Just a young boy from Capetown"
        James.my_story()
        ...
    
**Method:** stats(self)

*   Displays certain attributes of the Player instance that are related to its condition.
    
        # Exampale use
        ...
        James.stats()
        ...
        
**Method:** throw(self, item)

*   This function controls the act of disposing item from inventory 

*   The argument 'item' is used as a key to access the item from the bag attribute.

*   The function will remove the item from Player's bag attribute and will append the item into the items attribute of the Player's location attribute, which is a Room instances.
    
        # Example use
        ...
        James.throw("Pizza")
        ... 

**Method:** goto(self, new_location)   

*   This function controls the act of changing location

*   The argument 'new_location' is used as a key to access a Room instance from Player's location near_rooms attribute

*   Player's location is changed to the Room instances, Player can only travel to rooms that are in the near_room attribute of their current location
        
        # Example use
        ...
        James.goto("bathroom")
        ... 

**Method:** look_around(self)

*   This function controls the act of examining your surroundings
*   The function displays the description of the Player's current location, items, and the NPC instances

        # Example use
        
        ...
        James.look_around()
        ...
        
**Method:** eat(self, food)

*   Controls the act of eating food
*   The argument 'food' is used as a key to access the Food instance in the Player's bag attribute.
*   It will increase Player's hp attribute with the Food instance's regen attribute, then the Food instances will be deleted
  
        # Example use
        ...
        James.eat("Pizza")
        ...

**Method:** equip(self, armor)

*   Controls the act of equipping equipment
*   The argument 'armor' is used as a key to access the Armor instance in the Player's bag attribute.
*   It will switch the Player defence attribute with the Armor instance's defence value, then the Armor instance will be deleted

        # Examlple use
        ...
        from TBG.item import Armor
        
        shirt = Armor("Shirt", defence=2)
        
        James.bag[shirt.name] = shirt
        James.equip("Shirt")
        ...
       
 **Method:** learn(self, scroll)
 
 *  Controls act of learning the moves from a scroll
 *  The argument 'scroll' is used as a key to access the Scroll instance in the Player's bag attribute.
 *  It will replace the Player instance's fighting_move attribute will the Scroll instances fighting_move attribute, then it will be deleted
 
         # Example use
    
         from TBG.item import Scroll
         from TBG.fight_move import Fight
    
         Dragon_book = Scroll("Dragon_book")
         Dragon_book.desc = "This scroll will teach you the moves of the amazing kunfu master, Dragon bokie."
    
         # Our dictionary of Fight class instances
         punch = Fight("punch", damage_increase=10)
    
         dict =  {punch.name: punch}
    
         Dragon_book.fight_moves = dict
         
         James.bag[Dragon_book.name] = Dragon_book
         
         James.learn("Dragon_book")
         ...
         
**Method:**  enhance(self, enhancer)

*   Controls the act of increasing the damage dealt of a specific Fight class instance.
*   The argument 'enhancer' is used as a key to access the Enhancement instance in the Player's bag attribute.       
*   The function uses the Enhancement instance's damage attribute to increase the damage of Fight class instances that have the same value for the style attribute,  then it will be deleted.         

        # Example use
        
        from TBG.fight_move import Fight
        from TBG.item import Enhancement 
        
        punch = Fight("punch", damage=10, style="Normal")
        dumbbell = Enhancement("Dumbbell", damage_increase=10, style="Normal")
        
        James.fight_moves[punch.name] = punch
        James.bag[dumbbell.name] = dumbbell
        
        James.enhance("Dumbbell")
        
**Method:** show_move(self, move)

*   For displaying useful info about a Fight move.
*   The argument 'move' is used as a key to access the Fight instance in the Player's fight_moves attribute.       

        # Example use
        
        ...
        James.show_move("punch")
        ...
        
**Method:** talk(self, npc)

*   Controls the sct of conversing with NPC in the game
*   The argument 'npc' is used as a key to access the NPC instance in the Player's location's people attribute.       
*   Function will access the NPC's text_opt attribute and randomly select text to say back.

 
        # Example use 
        ...
        James.talk("Mum")
        ...
        
# Module: level

*   Contains the level class

### Class: Level

This class join s everything together and will allow us to explore the world and battle enemies.

     def __init__(self):
            self._level_rooms = None 
            self._command_variant = []  
            self._explore_help = "None"  # Help text for exploration method
            self._battle_help = "None"  # Help text for battle method 

*   **self._level_rooms:** Room instance, the first room that the player will be loaded in at the start of the level.
*   **self._command_variant:** A list of Cmd instances.
*   **self._battle_help:** Guide of how to play the game, explains the functionality of various verbs for exploring.
*   **self._explore_help:** Guide of how to play the game, explains the functionality of various verbs for battle.

**Method:** explore_loop(self, player, music_dir=None)

*   Handles "player" input and functionality for verbs

*   Argument player must be a Player instance.
*   Argument music_dir must be a directory to the music file that will play in the background.

The function will request the player for input, the input is processed through the list of Cmd instances 
breaker method, if match is found the corresponding function will b executed.

    from TBG.CMD import Cmd
    from TBG.level import Level
    from TBG.room import Room
    from TBG.item import Food
    
    # Cmd instance
    eat = Cmd("eat")
    eat.command_list = [r"(chow)(\s*)(?P<arg1>[\w\']*)", r"(consume)(\s*)(?P<arg1>[\w\']*)"]    
    
    # Room instance
    Bedroom =  Room("Bedroom")
    
    # Food instance
    Pizza = Food("Pizza", regeneration=10)
    James.bag[Pizza.name] = Pizza
    
    # level instance
    level1 = Level()
    
    # rooms of level
    level1.level_rooms = Bedroom
    
    # List of Cmd objects
    level1.command_variant = [eat]
    
    # explore_loop
    level1.explore_loop(James)
    
    >>> player_input =  "chow Pizza"
        command_verb = "eat"
        arg1 = "Pizza"
        
    >>> James.eat(arg1)


**Method:** battle_loop(self, player, enemy, music_dir=None)
      
*   Handles player input and functionality for verbs
*   Argument "player" must be a Player instance and the "enemy" argument must be an Enemy instance.
*   Argument music_dir must be a directory to the music file that will play in the background.

The function will request the player for input, the input is processed through the list of Cmd instances 
breaker method, if match is found the corresponding function will b executed.

>   The functionality is based on battling the enemy


    # Example use
    ...
    from TBG.fight_move import Fight
    from TBG.player import Enemy
    from TBG.CMD import Cmd
    
    # Cmd instance for battling
    attack = Cmd("attack")
    attack.command_list =  [r"(attack[\s]*with)(\s*)(?P<arg1>[\w\']*)", r"(use)(\s*)(?P<arg1>[\w\']*)"]
    
    punch = Fight("punch", damage=10, style="Normal")
    James.fight_moves[punch.name] = punch
    
    # enemy instance
    BadGuy = Enemy("BadGuy")
    BadGuy.fight_moves[punch.name] = punch
    
    level1.command_variant.append(attack)
    level1.battle_loop(player=James, enemy=BadGuy)


# Default help text

Explaining what each command does is quite redundant on your side, so I've created default help text that you can used
how your version of the game works.

The text is located in  default_help script, inside you will find 'def_ex_help' and 'def_b_help'. They contain text explaining
each command synonymy's use

        def_bat_help = """
        >> How to play?
        
        On playing the game you will see this 'Command: ' here you will
        input what you want to do next. There are multiple options to pick from
        based on your needs of battle.
        
        Command types:
        
        1.  Command: attack Name_of_fighting_move
        >   This command allows the user to used their fight move against an enemy.
            Input the command followed by the name of the fight move
        eg. Command: attack with Dragon_kick
        
        2. Command: eat Name_of_item
        >   This command is used to eat food from the game. 
            Input the command followed by the name of the item
        eg. Command: eat Pizza
        
        3.  Command: stats
        >   This command is used to display the attribute of the player.
        eg Command: abilities
        
        4. Command: show_move Name_of_fighting_move
        >   This command is used to display the attribute of a player's fighting move.
            Input the command followed by the name of the fight move
        eg. Command: skill Dragon_kick
            """
            
 ------------------           
            
           def_ex_help = """
        >> How to play?
        
        On playing the game you will see this 'Command: ' here you will
        input what you want to do next. There are multiple options to pick from
        based on your needs of exploration.
        
        Command types:
        
        1.  Command: look around 
        >   This command is used to display the items, people, exits available a Room.
        eg. Command: look around
        
        2.  Command: goto Name_of_Room
        >   This command is used to change the player's location/Room.
            Input the command followed by the name of the Room
        eg. Command: enter Johnny's_House
        
        3.  Command: take_item Name_of_item
        >   This command is used to take items from a Room.
            Input the command followed by the name of the item
        eg. Command: take Phone
        
        4.  Command: throw Name_of_item
        >   This command is used to throw away items from your inventory.
            Input the command followed by the name of the item
        eg. Command: throw away Phone
        
        5.  Command: examine/look at Name_of_item
        >   This command is used to display the attribute of an item from your inventory.
            Input the command followed by the name of the item.
        eg. Command: examine Phone 
        
        6.  Command: search_inv
        > This command is used to display the names of items that are in your inventory.
        eg. Command: search inventory
        
        7.  Command: stats
        >   This command is used to display the attribute of the player.
        eg Command: abilities
        
        8.  Command: my_story
        >   This command is used to display the players back story.
        eg Command: back story
        
        9.  Command: learn Name_of_item
        >   This command is used to give player a new set of fighting moves
            Input the command followed by the name of the item
        eg. Command: study Dragon_scroll
        
        10. Command: enhance Name_of_item
        >   This command is used to increase damage of player's fighting move set, provided
            that they are of the same style.
            Input the command followed by the name of the item
        eg. Command: train Dumbbell
        
        11. Command: show_move Name_of_fighting_move
        >   This command is used to display the attribute of a player's fighting move.
            Input the command followed by the name of the fight move
        eg. Command: skill Dragon_kick
        
        12. Command: equip Name_of_armor
        >   This command is allows the player to equip armor.
            Input the command followed by the name of the armor
        eg. Command: wear T-shirt
        
        13. Command: talk Name_of_NPC
        >   This command is used for talking to NPCs in the game
            Input the command followed by the name of NPC
        eg. Command: approach Mummy
        
        14. Command: eat
        >   This command is used to eat food from the game. 
            Input the command followed by the name of the item
        eg. Command: eat Pizza
            
        15. Command: proceed
        >   This command will end the game loop inorder to proceed.
        eg. Command: proceed
        
        """
  
 The text explains what the commands will do when playing the game.
 This section of the text '#No. Command: \<replace with your synonyms>' 
 
    >   eg.  14. Command: chow/munch/consume Name_of_item
             >   This command is used to eat food from the game. 
                 Input the command followed by the name of the item
          eg.Command: eat Pizza 