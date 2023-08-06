class SilentAction(object):
    """
    Create Silent Actions for Silent Message HSl

    Attributes
    ----------
    type : str
        Type of silent action.
        
    via_name : str
        via_name of the corresponding business.
        
        
    action_id : str
        id of the silent action.
        
    data : dict
        options that will be sent as payload
    """

    def __init__(self, action_type: str, id: int, via_name: str):
        self.type: str = action_type
        self.via_name: str = via_name
        self.action_id: int = id
        self.data: dict = {}

    def to_hsl(self) -> dict:
        """
        Generate HSL dict
        """
        self.data['Id'] = self.action_id
        self.data['via_name'] = self.via_name
        return {
            "type": self.type,
            "data": self.data
        }
