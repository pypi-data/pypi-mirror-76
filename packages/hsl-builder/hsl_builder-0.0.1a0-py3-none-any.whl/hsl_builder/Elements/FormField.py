from enum import Enum,unique
from typing import List

@unique
class FormFieldType(Enum):
    TEXT = 'text'
    PICKER = 'picker'
    TIME = 'time'
    DATE = 'date'
    CONTACT_PICKER = 'contactpicker'
    START_DATE = 'startdate'
    END_DATE = 'enddate'
    SEARCH = 'search'
    SEARCH_EDITABLE = 'searcheditable'
    SAVED_ADDRESS = 'savedaddress'
    DOB = 'dob'
    MULTI_DAY_PICKER = 'multidaypicker'
    MULTI_SELECT_PICKER = 'multiselectpicker'

@unique
class FormKeyboardType(Enum):
    NORMAL = 'normal'
    NUMBER = 'number'
    EMAIL = 'email'


class FormField(object):
    """
     Create FormField objects that can be added in the Form Object

    Attributes
    ----------
    key : str
        When the form is submitted, apps show the value for the form field against this key.
        This key will then be used for entity detection in bot builder

    type : FormFieldType
        The type of the formfield

    keyboard_type : FormKeyboardType
        The keyboard type used to fill the corresponding form

    order : int
        The order of the form

    icon : str 
        Icon name for the field.

    hint : str
        Input placeholder for the field

    options : str
        In case of FormField type picker or multiselectpicker
        These will be used as the options to pick from.

    search_source : str
        API URL to get the search results from

    search_placeholder : str
        placeholder when no text is entered for search type fields

    autofill : str 
        Auto fill field based on user profile or default value.

    auto_fill_source : str
        Source for the autofilling the field
    """
    def __init__(self, key: str, form_type: FormFieldType, order: int, hint: str, icon: str):
        self.key: str = key
        self.type: FormFieldType = form_type
        self.keyboard_type: FormKeyboardType = FormKeyboardType.NORMAL
        self.order: int = order
        self.icon: str = icon
        self.hint: str = hint
        self.options: List[str] = []
        self.search_source: str = ''
        self.search_placeholder: str = ''
        self.autofill: str = ''
        self.autofill_source: str = ''

    def to_hsl(self) -> dict:
        """
        returns an HSL dict for the form field
        """
        return {
            'key': self.key,
            'type': self.type.value,
            'keyboard_type': self.keyboard_type.value,
            'order': self.order,
            'icon': self.icon,
            'hint': self.hint,
            'options': self.options,
            'search_source': self.search_source,
            'search_placeholder': self.search_placeholder,
            'autofill': self.autofill,
            'autofill_source': self.autofill_source,
            #TODO: add regex fields
        }
