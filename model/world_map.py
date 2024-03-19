from model.map import Map

class WorldMap():
    _instance = None

    def __init__(self):
        if WorldMap._instance is not None:
            raise Exception("Singleton cannot be instantiated twice!")
        self.map_grid = {}  # Use a dictionary for coordinate-based lookup

    @staticmethod
    def get_instance():
        if WorldMap._instance is None:
            WorldMap()
        return WorldMap._instance