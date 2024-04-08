class Observer:
    def update(self, subject):
        raise NotImplementedError("Must be implemented by subclasses")
