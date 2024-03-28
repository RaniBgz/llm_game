from model.maps.map import Map
from view import view_constants as vcst

class LocalMap(Map):
    def __init__(self):
        super().__init__()
        self.items = []
        self.entities = []
        self.entities_dict = {}
        self.parent_map = None
        self.initialize_entities_dict()

    def initialize_entities_dict(self):
        for i in range(0, vcst.H_TILES):
            for j in range (0, vcst.V_TILES):
                self.entities_dict[(i, j)] = None

    def add_player(self, character):
        self.player = character
        self.player.location = (0, 0)  # Set the character's location on this map

    def add_entity(self, entity):
        self.entities_dict[entity.local_position] = entity
        # self.entities.append(entity)

    def remove_player(self):
        self.player = None
