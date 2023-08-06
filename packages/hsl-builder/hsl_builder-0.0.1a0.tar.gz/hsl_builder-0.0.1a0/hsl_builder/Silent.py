from .Base import BaseElement
from typing import List

from .Elements import SilentAction

class Silent(BaseElement):
    """
    Create Silent Message HSL

    Attributes
    ----------
    actions : List[SilentAction]
        list of silent acitons to be taken
    """
    def __init__(self,text: str):
        super().__init__(text,'SILENT')
        self.actions: List[SilentAction] = []

    def to_hsl(self):
        """
        Generate HSL dict
        """
        hsl = super().to_hsl()
        data = {
            'silent_actions': [action.to_hsl() for action in self.actions]
        }
        hsl['data'] = data

        return hsl
