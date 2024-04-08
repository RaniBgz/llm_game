from model.map.map import Map
from view import view_constants as vcst

class LocalMap(Map):
    def __init__(self):
        super().__init__()
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)