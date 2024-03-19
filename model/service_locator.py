
class ServiceLocator:
    def __init__(self):
        self.services = {}

    def register(self, service_name, instance):
        self.services[service_name] = instance

    def get(self, service_name):
        return self.services[service_name]