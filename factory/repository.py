from repository.response import ResponseRepository
from config.engine import DatabaseConfiguration


class RepositoryFactory:
    __slots__ = ["_response"]
    instance = None

    def __init__(self):
        self._response = None

    @property
    def response(self) -> ResponseRepository:
        if self._response is None:
            self._response = ResponseRepository(DatabaseConfiguration.get_engine())
        return self._response

    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = RepositoryFactory()
        return cls.instance

