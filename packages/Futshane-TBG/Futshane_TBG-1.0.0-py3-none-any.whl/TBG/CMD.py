# This module provides the class for extracting the players commands and divide them into useful pieces

import re


class Cmd:
    """ Used in the  "level" object to extract players's input and determine their action"""

    def __init__(self, name):
        self._command_list = []  # Contains the list of regex expression of related verbs or player commands
        self.name = name  # The name that will be used to determine player action/verb

    @property
    def command_list(self):
        """Returns a list of the regex patterns that are related"""
        return self._command_list

    @command_list.setter
    def command_list(self, listi):
        """setting the list of related regex patterns"""
        self._command_list = listi

    def breaker(self, txt):  # Takes player command and returns regex search object

        """Uses regex to break up the text into useful info"""
        """Returns  a search object which can be used to extract the info that you need"""

        for test in self.command_list:  # Iterating through the related list of regex patterns

            value = re.search(test, txt)

            if value:  # If the match is found the regex object will be return

                return value  # This will contain the info that you want to extract, require knowledge of re module

        else:  # If the whole list doesnt capture any info the function will return false

            return False
