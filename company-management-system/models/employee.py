from __future__ import annotations
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CHAR, ForeignKey
from sqlalchemy.orm import validates
from datetime import date
from settings import KIND_OPTS
from models.validators import validate_in_list, validate_type
from utils.input_manager import Input
from datetime import datetime
from models.base import Base


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(
        autoincrement=True, nullable=False, primary_key=True
    )
    name: Mapped[str] = mapped_column("name", nullable=False)
    job_title: Mapped[str] = mapped_column("job_title", nullable=False)
    gender: Mapped[CHAR] = mapped_column("gender", CHAR, nullable=False)  # m , f
    kind: Mapped[str] = mapped_column(
        "kind", String(20), nullable=False
    )  # full , part , free
    worked_hours: Mapped[List[WorkedHours]] = relationship(
        back_populates="employee", cascade="all, delete", lazy="subquery"
    )
    rewards: Mapped[List[Reward]] = relationship(
        back_populates="employee", cascade="all, delete", lazy="subquery"
    )

    @classmethod
    def get_input_list(cls) -> list[Input]:
        return [
            Input("name", str, str, "Name: "),
            Input("job_title", str, str, "Title: "),
            Input("gender", str, str, "Gender (m , f): ", call_back_funcs=[str.lower]),
            Input("kind", str, str, "Kind: ", call_back_funcs=[str.lower]),
        ]

    @validates("gender")
    def validate_gender(self, key, value: str) -> str:
        return validate_in_list(value.lower(), ["m", "f"])

    @validates("kind")
    def validate_kind(self, key, value: str) -> str:
        return validate_in_list(value.lower(), KIND_OPTS)

    def get_total_hours(self) -> float:
        print(self.worked_hours)
        return sum(x.hours for x in self.worked_hours)

    def __str__(self):
        return f"{self.id} - {self.name}"


class WorkedHours(Base):
    __tablename__ = "worked_hours"
    id: Mapped[int] = mapped_column(
        autoincrement=True, nullable=False, primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        "employee_id", ForeignKey("employees.id"), nullable=False
    )
    employee: Mapped["Employee"] = relationship(
        back_populates="worked_hours", lazy="subquery"
    )
    hours: Mapped[float] = mapped_column("hours", nullable=False)
    hour_rate: Mapped[float] = mapped_column("current_hour_rate", nullable=False)
    worked_date: Mapped[date] = mapped_column("worked_time", nullable=False)

    def __str__(self):
        return f"ID:{self.id} - {self.employee.name} - {self.hours} H - {self.hour_rate}$/H - {self.worked_date}"

    @classmethod
    def get_input_list(cls) -> list[Input]:
        return [
            Input(
                "worked_date",
                date,
                datetime.strptime,
                "Enter a date in the format YYYY-MM-DD: ",
                cast_func_args=["%Y-%m-%d"],
                call_back_funcs=[datetime.date],
            ),
            Input("hour_rate", float, float, "Enter Hour Rate Price: "),
            Input("hours", float, float, "Enter Hours Worked: "),
        ]

    def bill(self) -> float:
        return self.hours * self.hour_rate

    @validates("worked_date")
    def validate_worked_date(self, key, value) -> date:
        return validate_type(value, date)

    @validates("hours", "hour_rate")
    def validate_float(self, key, value) -> float:
        return validate_type(value, float)


class Reward(Base):
    __tablename__ = "rewards"
    id: Mapped[int] = mapped_column(
        autoincrement=True, nullable=False, primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        "employee_id", ForeignKey("employees.id"), nullable=False
    )
    employee: Mapped[Employee] = relationship(back_populates="rewards", lazy="subquery")

    value: Mapped[float] = mapped_column("value")
    reward_date: Mapped[date] = mapped_column("date")

    @classmethod
    def get_input_list(cls) -> list[Input]:
        return [
            Input("value", float, float, "Enter Reward Value: "),
            Input(
                "reward_date",
                date,
                datetime.strptime,
                "Enter a date in the format YYYY-MM-DD: ",
                cast_func_args=["%Y-%m-%d"],
                call_back_funcs=[datetime.date],
            ),
        ]

    @validates("date")
    def validate_worked_date(self, key, value) -> date:
        return validate_type(value, date)

    @validates("value")
    def validate_float(self, key, value) -> float:
        return validate_type(value, float)

    def __str__(self):
        return f"{self.id} - {self.employee.name} - {self.value}"
