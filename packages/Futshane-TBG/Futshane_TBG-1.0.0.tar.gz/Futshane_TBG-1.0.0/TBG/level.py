# This module contains the class for developing a level in the game

from random import randint as random
from typewriter import typewriter    # Substitute of the "print" function

# Importing pygame for musical features
try:
    from pygame import mixer, error

except ImportError:
    pass

# Initialising the mixer for playing background music
mixer.init()


def cleaner(f):  # Wrapper function
    """Makes printed text easier to read by creating border around the text"""

    def wrap(*args, **kwargs):
        print("==" * 20)
        f(*args, **kwargs)
        print("==" * 20)
        print("\n")

    return wrap


class Level:
    """ For creating the battle and exploration variables in a level"""

    def __init__(self):
        self._level_rooms = None  # The dictionary of related Room class instances
        self._command_variant = []  # A list of the CMD class instances
        self._explore_help = "None"  # Help text for exploration method
        self._battle_help = "None"  # Help text for battle method

    @property
    def level_rooms(self):
        """Returns a list of the Room class instances for the level"""
        return self._level_rooms

    @level_rooms.setter
    def level_rooms(self, listi):
        """setting the list of the Room class instances for the level"""
        self._level_rooms = listi

    @property
    def command_variant(self):
        """Return a list of a list of the CMD class instances for level"""
        return self._command_variant

    @command_variant.setter
    def command_variant(self, listi):
        """setting a list of the CMD class instances for level"""
        self._command_variant = listi

    @property
    def explore_help(self):
        """Returns the text that explains each command available for the exploration method"""
        return self._explore_help

    @explore_help.setter
    def explore_help(self, txt):
        """setting the text that explains each command available for the exploration method"""
        self._explore_help = txt

    @property
    def battle_help(self):
        """Return the text that explains each command available for the battle method"""
        return self._battle_help

    @battle_help.setter
    def battle_help(self, txt):
        """setting the text that explains each command available for the battle method"""
        self._battle_help = txt

    @cleaner
    def explore_loop(self, player, music_dir=None, start_pos=0.0):
        """ Take Player object and a music directory that will play in the back ground"""

        player.location = self.level_rooms  # Setting the Player object's initial location

        # Playing background music
        try:
            mixer.music.load(music_dir)
            mixer.music.play(-1, start_pos)

        except (TypeError, error):  # If music_dir is equal to "None"
            pass
        # =========================

        while True:

            # ==>Collecting players input/command
            player_input = input("Command: ")
            # ================================

            # ==>Running input through CMD objects to collect relevant info
            for command in self.command_variant:

                test = command.breaker(player_input)
                if test:  # Testing if input matches any CMD object

                    try:  # For input that has more to extract
                        command_verb = command.name  # Extracting the the player action/verb
                        arg1 = test.group("arg1")  # Object of the verb
                        break

                    except IndexError:  # If verb isn't paired with object

                        command_verb = command.name
                        break

            else:  # If player_input doesnt have match
                typewriter.typing("!!>Action/verb isn't understood<!!")
                continue
            # =====================================================

            # ==>effect of the players command
            if command_verb == "ex_help":
                typewriter.typing(self._explore_help, 0.0005)

            elif command_verb == "goto":
                # Change Player's location attribute
                player.goto(arg1)

            elif command_verb == "look_around":
                # display players location description
                player.look_around()

            elif command_verb == "examine_item":
                # Displays item description
                player.examine_item(arg1)

            elif command_verb == "throw":
                # Removing item from Player objects bag attribute
                player.throw(arg1)

            elif command_verb == "talk":
                # Print conversation text of NPC
                player.talk(arg1)

            elif command_verb == "take_item":
                # Removes item from Player object's location into bag attribute
                player.take_item(arg1)

            elif command_verb == "search_inv":
                # Displays Item objects that are in Player object's bag attribute
                player.search_inv()

            elif command_verb == "stats":
                # Displays useful info about the Player object
                player.stats()

            elif command_verb == "my_story":
                # Displays Player object's backstory attribute
                player.my_story()

            elif command_verb == "show_move":
                # Displays info about Player object's fight_move instance
                player.show_move(arg1)

            elif command_verb == "eat":
                # increase hp attribute of Player object
                player.eat(arg1)

            elif command_verb == "learn":
                # Changes the fighting_moves attribute of Player object
                player.learn(arg1)

            elif command_verb == "enhance":
                # increase the damage dealt of specific fight moves from Player's fighting_moves
                player.enhance(arg1)

            elif command_verb == "equip":
                # replaces the Player's defence value with Armor object's defence value
                player.equip(arg1)

            elif command_verb == "proceed":
                break

        #   Fade out of background music
        try:
            mixer.music.fadeout(1000)
        except (TypeError, error):
            pass
        # ==============================

    def battle_loop(self, player, enemy, music_dir=None, start_pos=0.0):
        """  Takes Player and Enemy objects and a music directory that will play in the back ground"""

        # Playing background music
        try:
            mixer.music.load(music_dir)
            mixer.music.play(-1, start_pos)

        except (TypeError, error):  # If music_dir is equal to "None"
            pass
        # =========================

        while True:

            # ==>Displaying Player object battle stats
            typewriter.typing(("==" * 20), 0.00085)
            typewriter.typing(f"=>{player.name}'s condition:", 0.00005)
            typewriter.typing(f"=>Health: {player.hp}")
            typewriter.typing(f"=>Defence: {player.defence} \n", 0.00005)
            # ========================================

            # ==>Displaying Enemy object battle stats
            typewriter.typing(f"==>>{enemy.name}'s condition:", 0.00005)
            typewriter.typing(f"=>Health: {enemy.hp}", 0.00005)
            typewriter.typing(f"=>Defence: {enemy.defence}", 0.00005)
            typewriter.typing(("==" * 20), 0.00085)
            # =======================================

            # ==>Collecting player input/command
            player_move = input("Command: ")
            # =================================

            # ==>Running input through CMD objects to collect relevant info
            for command in self.command_variant:

                test = command.breaker(player_move)
                if test:  # Testing if input matches any CMD object

                    try:  # For input that has more to extract
                        command_verb = command.name  # Extracting the the player action/verb
                        arg1 = test.group("arg1")  # Object of the verb
                        break

                    except IndexError:  # If verb is'nt paired with object

                        command_verb = command.name
                        break

            else:  # If player_input doesnt have match
                typewriter.typing("!!>Action/verb is'nt understood<!!")
                continue
            # =====================================================

            # ==>effects of player command"

            if command_verb == "show_move":
                # if player wishes to display  their fighting move and its description
                player.show_move(arg1)

            elif command_verb == "battle_help":
                typewriter.typing(self.battle_help, 0.00005)

            elif command_verb == "stats":
                # display players stats , mainly to show them their fighting moves
                player.stats()

            elif command_verb == "attack":
                # when player wishes use a move to fight enemy
                self._battle_math(player, enemy, arg1)

                # ==>ending if player or enemy is dead
                if player.hp <= 1:  # Testing if Player has 0 hp attribute

                    player.hp = 1  # setting player health to 1
                    typewriter.typing(f"=>{player.name} has been defeated")
                    typewriter.typing("=>YOU LOSE!!!")
                    return 0

                elif enemy.hp <= 1:  # Testing if Enemy has 0 hp attribute
                    typewriter.typing(f"=>{enemy.name} has been defeated")
                    typewriter.typing("=>YOU WIN!!!")
                    return 1
                # =====================================

            elif command_verb == "eat":
                # when player wants to increase their player
                player.eat(arg1)

            else:  # If player inputs a command not related to battle_loop
                typewriter.typing(f"!!>{command_verb} not a Battle scene action<!!")

        try:
            mixer.music.fadeout(1000)
        except (TypeError, error):
            pass

    def _battle_math(self, player, enemy, player_move):
        """ Displays the effects of the the Players fight_move and displays the effects"""

        # ==>>Player's move affects Enemy first
        if player_move in player.fight_moves:  # testing if the key to Player object's fight_moves is valid

            fight_move = player.fight_moves[player_move]  # Getting the fight_move object Player object

            typewriter.typing("\n>>" + "--" * 7 + f"{player.name}" + "--" * 7 + "<<", 0.035)
            index = len(fight_move.atck_desc)  # Getting len of attack descriptions list

            text = fight_move.atck_desc[random(0, index - 1)]  # Getting the attack description
            typewriter.typing(f"==>>{text} \n", 0.035)  # displaying the attack description

            self._damage_effect(player, enemy, player_move)  # calculates the effects of the move

            # testing if enemy is dead
            if enemy.hp < 1:
                return

        else:  # If key does'nt exist
            typewriter.typing(f"=>{player.name} does not know how to {player_move}")
            return 0
        # ===============================================================================================

        # enemy's turn to fight
        move_keys = list(enemy.fight_moves)  # length of enemy's fight_moves
        enemy_move = move_keys[random(0, len(move_keys) - 1)]  # random pick of enemy move from their list

        fight_move = enemy.fight_moves[enemy_move]  # Getting the fight_move object of Enemy object

        typewriter.typing("\n>>" + "--" * 7 + f"{enemy.name}" + "--" * 7 + "<<", 0.030)
        index = len(fight_move.atck_desc)  # Getting len of attack descriptions list

        text = fight_move.atck_desc[random(0, index - 1)]  # Getting the attack description
        typewriter.typing(f"==>>{text} \n", 0.090)  # displaying the attack description

        self._damage_effect(enemy, player, enemy_move)  # calculates the effects of the move
        # =============================================================

    @staticmethod
    def _percent_absorption(init_damage, after_damage):
        """ Calculates the percent of attack being absorbed by defence attributes"""

        numerator = init_damage - after_damage  # Numerator fro division
        denominator = init_damage  # Denominator fro division

        # calculation
        percentage = (numerator / denominator) * 100

        return str(round(percentage, 2))

    def _damage_effect(self, fighter, enemy, move):
        """ Calculates the values of the fight move used against an opponent"""

        damage = fighter.fight_moves[move].damage

        # defence affect
        if not (random(0, 1) == random(0, 1)) and enemy.defence != 0:
            damage -= enemy.defence  # Subtracting damage from defence value of opponent

            if damage < 1:  # If damage value results in a negative value
                damage = 1

            percent = self._percent_absorption(fighter.fight_moves[move].damage, damage)  # Calculating percent absorbed
            typewriter.typing(f"=>{enemy.name} blocked {percent}% of the attack")

        # subtracting enemy health by fighter damage
        enemy.hp -= damage
