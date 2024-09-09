class Signal:
    def __init__(self, task) -> None:
        self.task = task

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.task}>"

    def print(self):
        print(self)


class Succeeded(Signal):
    pass


class Cancelled(Signal):
    pass


class Failed(Signal):
    pass
