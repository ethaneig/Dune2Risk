
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.troops = 0
        self.territories = []
    
    def update_territories():
        self.territories = [territory for territory in territory if territory.owner == self]

class Continent:
    def __init__(self, name):
        self.name = name
        self.territories = [territory for territory in territory if territory.continent == self]

class Territory:
    def __init__(self, continent=0, troops=1, owner=None):
        self.continent = continent
        self.troops = troops
        self.owner = owner
        self.color = continentcolors[continent]