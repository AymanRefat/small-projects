from __future__ import annotations
from abc import abstractmethod
from sqlalchemy.orm import DeclarativeBase
from utils.input_manager import Input
from sqlalchemy.orm import Session
from sqlalchemy import Engine


class Base(DeclarativeBase):
    @abstractmethod
    def get_input_list(self) -> list[Input]:
        """Return list of inputs to get the data needed for creating or updating the obj"""

    @classmethod
    def _set_sessionmaker(self, sesionmaker: Session) -> Session:
        self.session = sesionmaker

    @classmethod
    def create_tabels(cls, engine: Engine) -> None:
        cls.metadata.create_all(engine)
