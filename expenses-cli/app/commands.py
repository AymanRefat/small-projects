from abc import ABC, abstractmethod
from argparse import _SubParsersAction
from enum import Enum

from app.expense_entry import ExpenseEntry
from app.json_manager import read_file, write_file


class Month(Enum):
    JANUARY = (1, "jan", "january")
    FEBRUARY = (2, "feb", "february")
    MARCH = (3, "mar", "march")
    APRIL = (4, "apr", "april")
    MAY = (5, "may", "may")
    JUNE = (6, "jun", "june")
    JULY = (7, "jul", "july")
    AUGUST = (8, "aug", "august")
    SEPTEMBER = (9, "sep", "september")
    OCTOBER = (10, "oct", "october")
    NOVEMBER = (11, "nov", "november")
    DECEMBER = (12, "dec", "december")

    def __new__(cls, month_number: int, short_name: str, full_name: str):
        obj = object.__new__(cls)
        obj._value_ = month_number
        obj.__setattr__("short_name", short_name)
        obj.__setattr__("full_name", full_name)
        return obj

    @classmethod
    def from_alias(cls, alias: str):
        """Convert an alias (number, short name, or full name) to an enum member."""
        alias = alias.lower()  # Normalize alias to lowercase
        for month in cls:
            if (
                alias == str(month.value)
                or alias == month.__getattribute__("short_name")
                or alias == month.__getattribute__("full_name")
            ):
                return month
        raise ValueError(f"Invalid month alias: {alias}")


class BaseCommand(ABC):
    name = "Base Command"
    description = "Base Command Description"
    help_text = "Base Command Help Text"
    success_message = "Base Command Success Message"
    error_message = "Base Command Error Message"

    def __init__(self, data: dict = {}):
        self.data = data
        self.parser = None

    @abstractmethod
    def install(self, parser: _SubParsersAction):
        pass

    def validate(self):
        """Return True or Raise Exception"""
        return True

    def add_data(self, data: dict):
        self.data.update(data)

    @abstractmethod
    def _run(self):
        pass

    def print_success_message(self):
        print(self.success_message)

    def print_error_message(self):
        print(self.error_message)

    def run(self):
        self.validate()
        try:
            self._run()
            self.print_success_message()
        except Exception as e:
            print(f"Error: {e}")
            self.print_error_message()
            return


class AddCommand(BaseCommand):
    name = "add"
    description = "Add Expense"
    help_text = "You can add Expense using this command"
    success_message = "Expense Added Successfully"
    error_message = "Error Adding Expense"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("amount", type=float, help="The amount of the expense")
        self.parser.add_argument(
            "-d", "--description", help="Description of the expense"
        )

    def _run(self):
        objs = read_file() or []
        expense_entry = ExpenseEntry.create(**self.data)
        objs.append(expense_entry.model_dump())
        write_file(objs)


class ListCommand(BaseCommand):
    name = "list"
    description = "List Expenses"
    help_text = "You can list expenses using this command"
    success_message = "expense List"
    error_message = "Error Listing expenses"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)

    def _run(self):
        objs = read_file() or []
        count = 0
        for obj in objs:
            expense_entry = ExpenseEntry(**obj)
            print(expense_entry)
            count += 1
        if count == 0:
            print("No entries found")


class UpdateCommand(BaseCommand):
    name = "update"
    description = "Update Expense Entry"
    help_text = "You can update expense entry using this command"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("id", type=int, help="Entry to be updated")
        self.parser.add_argument("-a", "--amount", type=float, help="New Amount")
        self.parser.add_argument(
            "-d", "--description", help="New description of the Expense"
        )

    def _run(self):
        expense_entry_list = read_file() or []
        old = None
        for entry in expense_entry_list:
            if entry["id"] == self.data["id"]:
                entry_obj = ExpenseEntry(**entry)
                entry_obj.update(
                    amount=self.data.get("amount", entry_obj.amount),
                    description=self.data.get("description", entry_obj.description),
                )
                old = entry

        # delete the old expense
        # add the new expense
        if old:
            expense_entry_list.remove(old)
            expense_entry_list.append(entry_obj.model_dump())
        else:
            print("Expense Entry not found")
        write_file(expense_entry_list)


class DeleteCommand(BaseCommand):
    name = "delete"
    description = "Delete Expense Entry"
    help_text = "You can delete expense using this command"
    success_message = "Expense Deleted Successfully"
    error_message = "Error Deleting Expense"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("id", type=int, help="Expense entry to be deleted")

    def _run(self):
        entry_list = read_file() or []
        old = None
        for entry in entry_list:
            if entry["id"] == self.data["id"]:
                old = entry

        # delete the old entry
        if old:
            entry_list.remove(old)

        write_file(entry_list)


class SummaryCommand(BaseCommand):
    name = "summary"
    description = "Summary of Expenses"
    help_text = "You can get summary of expenses using this command"
    success_message = "Summary of Expenses"
    error_message = "Error getting summary of expenses"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        mon_choices = (
            [month.short_name for month in Month]
            + [month.full_name for month in Month]
            + [str(month.value) for month in Month]
        )
        self.parser.add_argument(
            "-m", "--month", choices=mon_choices, help="Month to get summary"
        )

    def _run(self):
        objs = read_file() or []
        total = 0
        if month := self.data.get("month"):
            # sum the expenses for the month
            for obj in objs:
                expense_entry = ExpenseEntry(**obj)
                if expense_entry.created_at.month == Month.from_alias(month).value:
                    total += expense_entry.amount
        else:
            for obj in objs:
                expense_entry = ExpenseEntry(**obj)
                total += expense_entry.amount
        print(f"Total Expenses: {total}")
