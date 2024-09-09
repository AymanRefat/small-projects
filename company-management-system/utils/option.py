from abc import ABC, abstractmethod, abstractproperty
from utils.input_manager import Input
from utils.signal import *
from utils.funcs import combine_dicts
from models.employee import Base
import traceback


class Option(ABC):
    """an option is a function every Option should have a functionality to do"""

    name: str = None
    info: str = None
    model: Base = None
    input_list: list[Input] = []

    def __init__(self, exit_opt: bool = False) -> None:
        self.exit_opt = exit_opt
        self.data_dict = {}

    def get_input_list(self) -> list[Input]:
        return self.input_list

    @abstractproperty
    def task(self) -> str:
        """return a string describing the task"""

    def __str__(self) -> str:
        return self.name

    def show_info(self) -> None:
        if self.info:
            print(self.info)

    def get_data(self) -> None:
        """Take the data from the Input Manager and set it in the Option Instance"""
        data = []
        for item in self.get_input_list():
            data.append(item.try_till_get(self.exit_opt))
        self.data_dict = combine_dicts(*data)

    @abstractmethod
    def excute(self) -> None:
        """a function excutes when the user choose the option and return a Signal"""

    def add_signal(self, signal: Signal) -> None:
        self.signal = signal(self.task)

    def start(self) -> None:
        self.show_info()
        # to ensure that the opt needs data
        if len(self.get_input_list()) >= 1:
            self.get_data()
        try:
            self.excute()
            self.add_signal(Succeeded)
        except Exception as e:
            self.add_signal(Failed)
            with open("error.log", "w") as file:
                print(e)
                file.write(f"{e.__class__}: {e}")
                file.write(traceback.format_exc())

        self.signal.print()
