from utils.option import Option
from models.employee import Reward
from views.mixins import (
    CreateMixin,
    GetObjByIdMixin,
    DeleteMixin,
    ShowAllMixin,
)
from models.employee import Employee


class ShowAllRewards(ShowAllMixin, Option):
    name = "Show Rewards"
    info = "Rewards List"
    model = Reward


class CreateReward(GetObjByIdMixin, CreateMixin, Option):
    name = "Create Reward"
    model = Reward
    search_key = "employee_id"
    searched_model = Employee


class DeleteReward(DeleteMixin, Option):
    name = "Delete Reward"
    model = Reward
    searched_model = Reward
    search_key = "id"
