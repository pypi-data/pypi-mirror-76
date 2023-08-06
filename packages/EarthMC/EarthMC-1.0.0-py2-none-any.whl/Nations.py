import json, requests

class nations:
    def __init__(self):
        self.commands = ["all", "get"]
    def printCommands(self):
        for cmd in self.commands:
            print('\t%s ' % cmd)