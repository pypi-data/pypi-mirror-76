from typing import List

from .Elements.FormField import FormField


class Form(object):
    """
    Create HSL Form message.

    Attributes
    ----------
    title : str
        the title of the form.

    subtitle : str
        Sub title for the form for showing more info

    fields : List[FormField]
        list of formfields that will be added to the form

    """
    def __init__(self,text: str, subtitle: str):
        self.title: str = text
        self.type: str = 'FORM'
        self.subtitle: str = subtitle
        self.fields: List[FormField] = []

    def to_hsl(self):
        """
        Generate HSL dict
        """
        hsl = {
            'title': self.title,
            'type': self.type,
            'subtitle': self.subtitle
        }
        data = {
            'fields': [field.to_hsl() for field in self.fields]
        }
        hsl['data'] = data

        return hsl
