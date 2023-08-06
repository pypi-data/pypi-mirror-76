from .Base import BaseElement
from enum import unique,Enum

@unique
class SystemEvents(Enum):
    PINNED = 'chat_pinned'
    COMPLETE = 'chat_complete'

class System(BaseElement):
    """
    create system messages hsl

    Attributes
    ----------
    event_name : SystemEvents
        the type of the System Event to be sent

    payload : dict
        additonal data sent as payload
    """
    def __init__(self,text :str,event_name: SystemEvents):
        super().__init__(text,'SYSTEM')
        self.event = event_name
        self.payload = {}

    def to_hsl(self):
        hsl = super().to_hsl()
        data = {
            'event_name': self.event.value,
            'payload': self.payload
        }
        hsl['data'] = data

        return hsl
