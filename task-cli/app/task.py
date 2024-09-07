from datetime import datetime
from typing import ClassVar, Literal, Optional, Self

from pydantic import BaseModel, Field, PositiveInt
from pydantic.config import ConfigDict


class TaskManager:
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


class Task(BaseModel):
    model_config = ConfigDict(ser_json_timedelta="iso8601")
    id: PositiveInt = Field(default_factory=PositiveInt)
    name: str
    description: Optional[str] = ""
    status: Literal["todo", "doing", "done"]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Initialize the ID counter with the last saved ID
    _id_counter: ClassVar[int] = TaskManager.load_last_id()

    @classmethod
    def create(
        cls,
        name: str,
        status: Literal["todo", "doing", "done"] = "todo",
        description: str = "",
        **kwargs,
    ) -> Self:
        # Increment the ID counter
        cls._id_counter += 1
        TaskManager.save_last_id(cls._id_counter)
        return cls(
            id=cls._id_counter,
            name=name,
            description=description,
            status=status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def update(
        self,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
        new_status: Optional[Literal["todo", "doing", "done"]] = None,
        **kwargs,
    ):
        if new_name:
            self.name = new_name
        if new_description:
            self.description = new_description
        if new_status:
            self.status = new_status
        self.updated_at = datetime.now()

    def __str__(self):
        return f"{self.id} - {self.name} - {self.status} - {self.created_at} - {self.updated_at}"
