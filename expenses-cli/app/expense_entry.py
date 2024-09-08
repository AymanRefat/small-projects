from datetime import datetime
from typing import ClassVar, Optional

from pydantic import BaseModel, Field, PositiveInt
from pydantic.config import ConfigDict


class ExpensesManager:
    id_file = "last_id.txt"

    @classmethod
    def load_last_id(cls) -> int:
        try:
            with open(cls.id_file, "r") as f:
                res = f.read().strip()
                if res.isdigit():
                    return int(res)
                return 0
        except FileNotFoundError:
            return 0  # If file doesn't exist, start with ID 0

    @classmethod
    def save_last_id(cls, last_id: int):
        with open(cls.id_file, "w") as f:
            f.write(str(last_id))


class ExpenseEntry(BaseModel):
    model_config = ConfigDict(ser_json_timedelta="iso8601")
    id: PositiveInt = Field(default_factory=PositiveInt)
    amount: float
    description: Optional[str] = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Initialize the ID counter with the last saved ID
    _id_counter: ClassVar[int] = ExpensesManager.load_last_id()

    @classmethod
    def create(
        cls,
        amount: float,
        description: str = "",
        **kwargs,
    ):
        # Increment the ID counter
        cls._id_counter += 1
        ExpensesManager.save_last_id(cls._id_counter)
        return cls(
            id=cls._id_counter,
            amount=amount,
            description=description,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        self.updated_at = datetime.now()

    def __str__(self):
        return f"{self.id} - {self.amount} - {self.description} - {self.created_at} - {self.updated_at}"
