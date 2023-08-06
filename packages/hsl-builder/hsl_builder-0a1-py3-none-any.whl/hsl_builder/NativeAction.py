from .Base import BaseElement


class NativeAction(BaseElement):
    """
    Create Native Action HSL Message.
    Native Actions are used to communicate with the parent app in which SDK is integrated

    Attributes
    ----------
    method : str
        the method name for the native action 
    """
    def __init__(self,text: str, method: str):
        super().__init__(text,'NATIVE_ACTION')
        self.method = method

    def to_hsl(self):
        """
        Generate HSL dict
        """
        hsl = super().to_hsl()
        data = {
            'method': self.method
        }
        hsl['data'] = data

        return hsl
