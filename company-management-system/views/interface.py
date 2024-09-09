from sqlalchemy.orm import Session
from utils.menu import Menu
from settings import EXIT_OPT
from utils.input_manager import Input


class Interface:
    """a Class that managing the displaying of the menus"""

    choose = Input("choose", int, int, "Choose Option: ")

    def __init__(
        self,
        home_menu: Menu,
    ) -> None:
        self.home_menu = home_menu
        self.menu_history = []

    def start(self) -> None:
        self.print_welcome_message()
        if EXIT_OPT:
            print("'q' for Quit")
        self.start_menu(self.home_menu)

    def add_menu_to_history(self, menu: Menu) -> None:
        if len(self.menu_history) == 0:
            self.menu_history.append(menu)
        else:
            if self.menu_history[-1] != menu:
                self.menu_history.append(menu)

    def back_Menu(self) -> Menu:
        if self.menu_history:
            return self.menu_history[-2]

    def start_menu(self, menu: Menu) -> None:
        self.add_menu_to_history(menu)
        menu.display()
        back_opt_num = None

        if len(self.menu_history) >= 2:
            back_opt_num = menu.range_opt_number[1] + 1
            print(f"{back_opt_num}. Back")

        choose = self.choose.try_till_get(exit_opt=EXIT_OPT).get("choose")
        if choose == back_opt_num:
            self.start_menu(self.back_Menu())
        else:
            opt = menu.get_opt(choose)

            # if it was a new menu
            # show it
            # if it's a command do it

            if isinstance(opt, Menu):
                self.start_menu(opt)
            else:
                opt(exit_opt=EXIT_OPT).start()
                self.start_menu(menu)

    def print_welcome_message(self) -> None:
        print("""======================================""")
        print("""=========== Welcome There ============""")
        print("""======================================""")
