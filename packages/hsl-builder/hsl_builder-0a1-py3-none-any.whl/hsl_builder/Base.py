class BaseElement(object):
    """
    Base Class containing common properties for all HSL Messages

    Attributes
    ----------
    text : str
        text for the message to be displayed to the user

    type : str
        type of the HSL Message

    voice_text : str
        this text will be spoken out if tts is enabled
    """

    def __init__(self, text: str, hsl_type: str):
        self.text: str = text
        self.type: str = hsl_type
        self.voice_text: str = ""

    def to_hsl(self):
        """
        Generate HSL dict
        """
        return {
            'text': self.text,
            'type': self.type,
            'voice_text': self.voice_text
        }
