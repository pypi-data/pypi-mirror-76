from enum import unique,Enum

@unique
class URI(Enum):
    """
    URI Types for showing which screen to open in case of app_action
    """
    NONE = ''
    SEND_LOCATION = 'SEND_LOCATION'
    CAROUSEL_DETAIL = 'CAROUSEL_DETAIL'
    GALLERY_PICKER = 'GALLERY_PICKER'
    IMAGE_UPLOAD = 'IMAGE_UPLOAD'
    DOCUMENT_PICKER = 'DOCUMENT_PICKER'
    LAUNCH_CHANNEL = 'LAUNCH_CHANNEL'
    LINK = 'LINK'
    SELF_SERVE_WEB = 'SELF_SERVE_WEB'


@unique
class ActionableType(Enum):
    """
    Actionable Types for specifying what action should be taken 
    """
    APP_ACTION = 'APP_ACTION'
    MESSAGE_BAR = 'MESSAGE_BAR'
    TEXT_ONLY = 'TEXT_ONLY'
    FORM_SHOW = 'FORM_SHOW'
    SHARE_RECEIPT = 'SHARE_RECEIPT'
    APP_FEEDBACK = 'APP_FEEDBACK'
    SHARE = 'SHARE'
 
class Actionable(object):
    """
    Create Actionables to be used in Buttons or Text messages

    Attributes
    ----------
    text : str
        Text for the Actionable that will be displayed on the CTA (button, quick reply,etc).
        
    type : ActionableType
        The type of `ActionableType`.
        
    type : URI
        The type of `URI`.
        
    location_required : bool
        True if location is required for using the Actionable.

    is_default : bool
        if True, on click of the element, this actionable will get triggered.

    payload : dict 
        optional payload containing metadata that might be needed by the Actionable
    """

    def __init__(self, text: str, type: ActionableType, uri: URI):
        self.text: str = text
        self.type: ActionableType = type
        self.uri: URI = uri
        self.location_required: bool = False
        self.is_default: bool = False
        self.payload: dict = {}

    def to_hsl(self) -> dict:
        """
        Generate HSL dict
        """
        return {
            'actionable_text': self.text,
            'type': self.type.value,
            'uri': self.uri.value,
            'is_default': 1 if self.is_default else 0,
            'location_required': self.location_required,
            'payload': self.payload
        }
