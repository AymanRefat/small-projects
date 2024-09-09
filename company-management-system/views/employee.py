from utils.option import Option
from models.employee import Employee
from settings import KIND_OPTS
from views.mixins import (
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
    ShowAllMixin,
)


class ShowAllEmployeesOpt(ShowAllMixin, Option):
    name = "Show all"
    info = "Employees List"
    model = Employee


class CreateNewEmployeesOpt(CreateMixin, Option):
    name = "Create New"
    info = f"Avaliable Kinds: {KIND_OPTS}"
    model = Employee


class UpdateEmployeesOpt(UpdateMixin, Option):
    name = "Update"
    info = f"Avaliable Kinds: {KIND_OPTS}"
    model = Employee
    search_key = "id"
    searched_model = Employee


class DeleteEmployeesOpt(DeleteMixin, Option):
    name = "Delete"
    model = Employee
    search_key = "id"
    searched_model = Employee
