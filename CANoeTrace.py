from typing import List, Union, Optional

from PythonCanoe.CANoeMessage import CANoeMessage


class CANoeTrace:
    """
    Description: Responsible for reading signals in trace window
    """
    def __init__(self, canoe_instance):
        if not canoe_instance:
            raise Exception("CANoe instance required for initializing trace class.")

        self.canoe_instance = canoe_instance
        self.messages: List[CANoeMessage] = []
        self.canoe_bus = canoe_instance.Bus

    def get_message_value_on_can_bus(self, message: CANoeMessage) -> Optional[str]:
        """
        Returns data of message if valid message
        Returns None if message is invalid and not found
        """
        try:
            self._verify_message_type_(message)
            res = self.canoe_bus.GetSignal(message.channel, message.message, message.signal)
            return str(res.Value)
        except:
            return None

    @classmethod
    def _verify_message_type_(cls, messages):
        if type(messages) != CANoeMessage:
            raise TypeError(f"Expected type: List[CANoeMessage] or CANoeMessage, got {type(messages)}")
