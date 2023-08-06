from .Actionable import Actionable
from typing import List

class CarouselItem(object):
    """
    Create Carousel Items for Carousel

    Attributes
    ----------
    title : str
        Title of specific carousel item.
        
    subtitle : str
        Subtitle of specific carousel item.
        
    description : str
        More verbose description of item that is shown below the subtitle

    actionables : List[Actionable]
        Actionables to be performed when the user taps on the item

    meta : str
        meta value for the corresponding carousal item
    """


    def __init__(self,title: str, subtitle: str):
        self.title: str = title
        self.subtitle: str = subtitle
        self.description: str = ''
        self.thumbnail: str = ''
        self.actionables: List[Actionable] = []
        self.meta: str = ''

    def to_hsl(self) -> dict:
        """
        Generate HSL dict
        """
        return {
            'title': self.title,
            'sub_title': self.subtitle,
            'description': self.description,
            'actionables': [actionable.to_hsl() for actionable in self.actionables],
            'meta': self.meta,
            'thumbnail': {
                'image': self.thumbnail
                }
        }
