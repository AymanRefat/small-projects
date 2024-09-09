from utils.option import Option
from models.employee import Employee, WorkedHours
from views.mixins import CreateMixin, GetObjByIdMixin, DeleteMixin, ShowAllMixin


class ShowWorkedHours(ShowAllMixin, Option):
    name = "Show All"
    info = "Worked Hours List"
    model = WorkedHours


class addWorkedHoursForAll(CreateMixin, Option):
    name = "Add Worked Hours for All "
    model = WorkedHours

    @property
    def task(self) -> str:
        return f"Adding {self.data_dict.get('hours')} with Hour Rate {self.data_dict.get('hour_rate')}$ For All Employees "

    def excute(self) -> None:
        with self.get_model().session as session:
            employees = session.query(Employee).all()
            for em in employees:
                self.data_dict["employee_id"] = em.id
                super().excute()


class addWorkedHoursForEmployee(GetObjByIdMixin, CreateMixin, Option):
    name = "Add Worked Hours for Employee"
    model = WorkedHours
    searched_model = Employee
    search_key = "employee_id"

    @property
    def task(self) -> str:
        return f"Adding {self.data_dict.get('hours')} with Hour Rate {self.data_dict.get('hour_rate')}$ For {self.get_obj()} "


class ShowTotalHoursForAll(ShowAllMixin, Option):
    name = "Show Total Hours for All"
    model = Employee

    @property
    def task(self) -> str:
        super().task + "Total Hours"

    def show(self, obj: Employee) -> None:
        print(f"{obj} - {obj.get_total_hours()}")


class DeleteWorkedHoursForEmployee(DeleteMixin, Option):
    name = "Delete Worked Hours for Employee"
    model = WorkedHours
    search_key = "employee_id"
    searched_model = Employee
