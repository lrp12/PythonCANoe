import time

import win32com


class CanoeMeasurement:

    def __init__(self, canoe_instance, canoe_app):
        self.canoe_app = canoe_app
        self.canoe_instance = canoe_instance
        self.canoe_measurement = canoe_instance.Measurement

    def is_running(self):
        return self.canoe_measurement.Running == 1

    def start(self):
        if not self.canoe_app.capl._registered:
            print("Functions need to be registered before starting measurement.")
            return

        self.add_on_init_handler()
        self.canoe_measurement.Start()
        while not self.is_running():
            time.sleep(1)

    def add_on_init_handler(self):
        from PythonCanoe.PythonCanoe import MeasurementInitHandler
        win32com.client.WithEvents(self.canoe_measurement, MeasurementInitHandler)

    def stop(self):
        if not self.is_running():
            print("Measurement not running.")
            return
        self.canoe_measurement.Stop()