from factory.service import ServiceFactory


class ControllerFactory:
    __slots__ = ["telegram", "service_factory"]
    instance = None

    def __init__(self):
        self.service_factory = ServiceFactory.get()

    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = ControllerFactory()
        return cls.instance

