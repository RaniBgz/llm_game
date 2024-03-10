""" Defines the character class that is used to define """

class Character:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def attack(self, other_character):
        other_character.hp -= self.damage
        print(f"{self.name} attacked {other_character.name}")