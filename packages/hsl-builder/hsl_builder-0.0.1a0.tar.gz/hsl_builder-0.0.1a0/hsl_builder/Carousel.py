from enum import Enum,unique
from typing import List

from .Base import BaseElement
from .Elements.CarouselItem import CarouselItem

@unique
class CarouselWidth(Enum):
    THIN = 'THIN'
    MEDIUM = 'MEDIUM'
    FAT = 'FAT'
    BIG = 'BIG'


class Carousel(BaseElement):
    """
    Create Carousel HSL message

    Attributes
    ----------
    aspect_ratio : float
        used to determine the height of the carousel

    width : `CarouselWidth`
        The width of each carousel Item

    items : List[CarouselItem]
        list of carousel items for the carousel
    """
    def __init__(self,text):
        super().__init__(text,'CAROUSEL')
        self.aspect_ratio: float = 1.0
        self.width: CarouselWidth = CarouselWidth.THIN
        self.items: List[CarouselItem] = []

    def to_hsl(self):
        """
        Generate HSL dict
        """
        hsl = super().to_hsl()
        data = {
            'image_aspect_ratio': self.aspect_ratio,
            'width': self.width.value,
            'items': [item.to_hsl() for item in self.items]
        }
        hsl['data'] = data

        return hsl
