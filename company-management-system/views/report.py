from utils.option import Option
from views.mixins import ShowAllMixin
from models.employee import Employee


class ShowFullReportforAll(ShowAllMixin, Option):
    model = Employee
    name = "Show all Reports"

    def excute(self) -> None:
        q: list[Employee] = self.get_objects()

        for em in q:
            total_worked_hours = 0
            total_rewards = 0
            em_worked_hours = em.worked_hours
            total_worked_hours = sum(h.bill() for h in em_worked_hours)
            em_rewards = em.rewards
            total_rewards = sum(r.value for r in em_rewards)
            print(
                f"Employee:{em} - Total Work {total_worked_hours}$ - Total Rewards {total_rewards}$"
            )
