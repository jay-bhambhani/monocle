import abc
from dataclasses import dataclass
from typing import Dict


@dataclass
class MonocleBackend(abc.ABC):
    pass


@dataclass
class PostgresBackend(MonocleBackend):

    user: str
    db: str
    host: str
    password: str
    port: int = 5432


class MonocleConfig:

    def __init__(self, backend: MonocleBackend):
        self.backend = backend

    @classmethod
    def load_cls(cls, yml: Dict):
        cls(
            backend=cls._get_backend(yml)
        )

    @classmethod
    def _get_backend(cls, yml: Dict):
        if yml['backend']['type'] == 'postgres':
            return PostgresBackend(
                host=yml['backend']['host'],
                user=yml['backend']['user'],
                db=yml['backend']['db'],
                password=yml['backend']['password'],
                port=yml['backend'].get('port', 5432)
            )
