from model.observer.observer import Observer


class GameControllerObserver(Observer):
    '''Use comments to define conventions for order of arguments and keywords'''
    def update(self, subject, *args, **kwargs):
        if args:
            print("args:", args)
        if kwargs:
            print("kwargs:", kwargs)
