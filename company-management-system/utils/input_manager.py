from typing import Callable, Any


class Input:
    def __init__(
        self,
        key: str,
        t: type,
        cast_func: Callable,
        promt_msg: str,
        cast_func_args: tuple = (),
        cast_func_kwargs: dict = {},
        call_back_funcs=[],
    ) -> None:
        self.t = t
        self.cast_func: Callable = cast_func
        self.promt_msg: str = promt_msg
        self.key = key
        self.cast_func_args: tuple = cast_func_args
        self.cast_func_kwargs: dict = cast_func_kwargs
        self.call_back_funcs: Callable = call_back_funcs

    def try_till_get(self, exit_opt=False) -> dict:
        """start a while loop until getting the data , returns a dict with the key and gotten data"""

        while True:
            data = input(self.promt_msg)
            if exit_opt:
                if data == "q":
                    print("Bye :)")
                    exit()
            try:
                return {self.key: self._cast(data)}
            except Exception as e:
                print(e)

    def _cast(self, value) -> Any:
        value = self.cast_func(value, *self.cast_func_args, **self.cast_func_kwargs)
        for func in self.call_back_funcs:
            value = func(value)
        return value
