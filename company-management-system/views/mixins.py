from utils.input_manager import Input
from models.employee import Base
from sqlalchemy.orm import Query


class BaseMixin:
    model: Base = None

    def get_model(self) -> Base:
        if self.model:
            return self.model
        else:
            raise ValueError("You need to add model attr to your class Option")


class ShowAllMixin(BaseMixin):
    @property
    def task(self) -> str:
        return f" Showing all {self.get_model().__name__}"

    def get_objects(self) -> list[object]:
        with self.get_model().session as session:
            return session.query(self.get_model()).all()

    def excute(self) -> None:
        q = self.get_objects()
        if len(q) == 0:
            print("Empty!")
        else:
            for x in q:
                self.show(x)

    def show(self, obj) -> None:
        print(obj)


class LoadInputMixin(BaseMixin):
    def get_input_list(self) -> list[Input]:
        return super().get_input_list() + self.get_model().get_input_list()


class CreateMixin(LoadInputMixin, BaseMixin):
    @property
    def task(self) -> str:
        return f"Creating New {self.get_model().__name__} Data:{self.data_dict}"

    def excute(self) -> None:
        """Create the object using the data dict"""
        model = self.get_model()
        with model.session as session:
            session.add(model(**self.data_dict))
            session.commit()


class GetObjByIdMixin(BaseMixin):
    search_key: str = None
    searched_model: Base = None

    def get_searched_model(self) -> Base:
        """"""
        if self.searched_model:
            return self.searched_model
        else:
            raise ValueError("You need to add searched_model attr to your class Option")

    def get_input_list(self) -> str:
        return super().get_input_list() + [
            Input(
                self.search_key,
                int,
                int,
                f"Enter the Id of {self.searched_model.__name__}: ",
            )
        ]

    def get_query(self) -> Query:
        model = self.get_searched_model()
        with model.session as session:
            return session.query(model).filter(
                getattr(model, self.search_key) == self.data_dict.get(self.search_key)
            )

    def get_obj(self) -> object:
        return self.get_query().one()


class UpdateMixin(GetObjByIdMixin, LoadInputMixin):
    @property
    def task(self) -> str:
        return f"Updating {self.get_obj()} to Be {self.data_dict}"

    def excute(self) -> None:
        with self.get_model().session as session:
            obj = self.get_obj()
            for k, v in self.data_dict.items():
                setattr(obj, k, v)
            session.commit()


class DeleteMixin(GetObjByIdMixin):
    @property
    def task(self) -> str:
        return f"Deleting {self.get_obj()}"

    def excute(self) -> None:
        with self.get_model().session as session:
            session.delete(self.get_obj())
            session.commit()
