import json, requests

def find(pred, iterable):
    for element in iterable:
        if pred(element):
            return element
    return None

class towns:
    def __init__(self):
        self.commands = ["all", "get"]
    def printCommands(self):
        for cmd in self.commands:
            print('\t%s ' % cmd)
    def get(self, townName):
        res = requests.get("https://earthmc.net/map/up/world/earth/")
        data = json.loads(res)

        foundPlayer = find(lambda x: x.get("name") == townName, data.get("players", []))
        print(foundPlayer)
