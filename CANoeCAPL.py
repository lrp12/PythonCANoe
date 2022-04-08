import time
from typing import List, Union


class CAPL:
    def __init__(self, canoe_app):
        if not canoe_app.canoe_instance:
            raise Exception("CANoe instance required for initializing trace class.")

        self.canoe_app = canoe_app
        self.canoe_instance = self.canoe_app.canoe_instance

        self.canoe_capl = self.canoe_instance.CAPL

        self._registered = False
        self.functions = []
        self.compiled_functions = {}
        self.compile()

    def compile(self):
        print("Compiling...")
        self.canoe_capl.Compile()

    def functions_registered(self) -> List[str]:
        """
        Note: This function is required to be called before starting measurement
        Returns list of functions registered
        Only registered functions can be called on runtime
        """
        self._registered = True
        return self.functions

    def register_function(self, function_name: Union[List[str], str]):
        """
        Adds functions which are then compiled (if found in can file) after measurement has started.
        Note: Functions can only be registered before starting measurement
        """
        if self.canoe_app.measurement.is_running():
            raise Exception("Functions can only be registered before starting measurement.")

        if type(function_name) != list and type(function_name) != str:
            raise TypeError(f"Function names should be a list of str or str. Got {type(function_name)}")

        if type(function_name) == str:
            self.functions.append(function_name)
        else:
            self.functions.extend(function_name)

    def call_function(self, function_name: str, *args):
        if function_name not in self.functions:
            raise AttributeError("Not a registered function.")

        func = self.compiled_functions.get(function_name)
        if args:
            kwargs = self._convert_args_to_kwargs_(args)
            res = func.Call(**kwargs)
        else:
            res = func.Call()

        # delay added to prevent destroying stack before function call is completed
        time.sleep(1)
        return res

    @classmethod
    def _convert_args_to_kwargs_(cls, *args) -> dict:
        if len(*args) > 10:
            raise Exception(f"Only upto 10 arguments are allowed. Received {len(*args)} arguments.")
        kwargs = {}
        for i, _arg in enumerate(*args):
            kwargs[f"p{i + 1}"] = _arg
        return kwargs
