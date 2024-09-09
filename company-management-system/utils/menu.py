from __future__ import annotations
from utils.option import Option


class Menu:
    """A Menu is Box contains a Number of Options , it organizes the displaying of them automatically and provide a way for choosing the option"""

    def __init__(self, name: str, *options: list[Option]) -> None:
        self.name = name
        self.options = options
        self.table = enumerate(options, 1)
        self._list = list(self.table)

    def display(self):
        for i, opt in self._list:
            print(f"{i}. {opt.name}")

    @property
    def range_opt_number(self) -> tuple(int, int):
        """Return Tuple of two numbers (First opt , Last opt)"""
        return (self._list[0][0], self._list[-1][0])

    def is_right_opt_num(self, num: int) -> bool:
        """return True if the chosen num between the range of the menu , return False if the chosen num out of the range of the menu"""

        return num in range(self.range_opt_number[0], self.range_opt_number[1] + 1)

    def get_opt(self, num: int) -> Option:
        """Gets the chosen Option"""
        ls = self._list

        # Because we start the Menu with 1
        if self.is_right_opt_num(num):
            opt = ls[num - 1][1]
            return opt
        else:
            # if was one opt
            if self.range_opt_number[0] == self.range_opt_number[1]:
                msg = f"the Number should be {self.range_opt_number[0]}"
            else:
                msg = f"the Number should be in range of {self.range_opt_number}"

            raise ValueError(msg)
