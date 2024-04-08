import uuid
from abc import ABC, abstractmethod



class Entity(ABC):
    def __init__(self):
        self.id = uuid.uuid4()
        # self._observers = []

    # def attach(self, observer):
    #     self._observers.append(observer)
    #
    # def detach(self, observer):
    #     self._observers.remove(observer)
    #
    # def notify(self):
    #     for observer in self._observers:
    #         observer.update(self)