from model.entity import Entity

class Object(Entity):
    def __init__(self, name, description, location, takeable=False):
        super().__init__()
        self.location = location
        self.takeable = takeable

