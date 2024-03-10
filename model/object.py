from model.entity import Entity

class Object(Entity):
    def __init__(self, name, description, location, takeable=False):
        super().__init__(name, description)
        self.location = location
        self.takeable = takeable

