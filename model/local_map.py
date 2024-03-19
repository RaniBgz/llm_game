from model.map import Map

class LocalMap(Map):
    def __init__(self):
        super().__init__()
        self.items = []
        self.npcs = []
