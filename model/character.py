""" Defines the character class that is used to define """
from model.entity import Entity

class Character(Entity):
    def __init__(self, name, description, hp):
        super().__init__(name, description)
        self.hp = hp
