from typing import List
from .Base import BaseElement
from .Elements.Actionable import Actionable

class Text(BaseElement):
    """
    Create simple text message HSL
    """
    def __init__(self,text):
        super().__init__(text,'TEXT')
        self.quick_replies: List[Actionable] = []
    def to_hsl(self):
        """
        Generate HSL message
        """
        hsl = super().to_hsl()
        data = {
            'quick_replies': [qr.to_hsl() for qr in self.quick_replies]
        }
        hsl['data'] = data

        return hsl
