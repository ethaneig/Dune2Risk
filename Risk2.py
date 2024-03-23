
import random
import numpy as np



class Board:


    def __init__(self, size):
        self.size = size
        self.countries = []


class Country:


    def __init__(self, name, player, connections):
        self.name = name
        self.player = player
        self.connections = {}
