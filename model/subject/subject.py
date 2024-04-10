from abc import ABC, abstractmethod

class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass

    # def notify(self):
    #     for observer in self._observers:
    #         observer.update(self, *args, **kwargs)
