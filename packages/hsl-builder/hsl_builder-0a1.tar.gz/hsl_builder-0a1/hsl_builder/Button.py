from typing import List
from .Base import BaseElement
from .Elements.Actionable import Actionable

class Button(BaseElement):
    """
    Create Button HSL Elements

    Attributes
    ----------
    actionables : List[Actionable]
        list of actionables that will be added to the button

    """
    def __init__(self,text):
        super().__init__(text,'BUTTON')
        self.actionables: List[Actionable] = []

    def to_hsl(self):
        """
        Generate HSL dict
        """
        hsl = super().to_hsl()
        data = {
            'items': [actionable.to_hsl() for actionable in self.actionables]
        }
        hsl['data'] = data

        return hsl
