
from model.character import Character
from model.item import Item
from model.object import Object
import random  # For a bit of randomness later
from view.game_interface import GameInterface


if __name__ == "__main__":
    app = GameInterface()
    app.run()

