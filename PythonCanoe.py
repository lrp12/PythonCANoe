import os.path

from win32com.client import DispatchEx

from PythonCanoe.CANoeCAPL import CAPL
from PythonCanoe.CANoeMeasurement import CanoeMeasurement
from PythonCanoe.CANoeTrace import CANoeTrace

canoe_app = None


class MeasurementInitHandler:

    def OnInit(self):
        global canoe_app
        for func in canoe_app.capl.functions:
            res = canoe_app.capl.canoe_capl.GetFunction(func)
            canoe_app.capl.compiled_functions[func] = res


class CanoeApp:

    def __init__(self, config_file_path: str):
        # self.canoe_app = get_canoe_instance()
        # self.canoe_app = DispatchEx('CANoe.Application')

        self.canoe_instance = DispatchEx('CANoe.Application')

        if not os.path.exists(config_file_path):
            raise FileNotFoundError("Config file not found")

        self.canoe_instance.Open(config_file_path)

        # initializing modules
        self.trace = CANoeTrace(self.canoe_instance)
        self.capl = CAPL(self)
        self.measurement = CanoeMeasurement(self.canoe_instance, self)

        global canoe_app
        canoe_app = self

        self.canoe_instance.CAPL.Compile()

    def get_config_open_status(self):
        status = self.canoe_instance.Configuration.OpenConfigurationResult.result
        return status

