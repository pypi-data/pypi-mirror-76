from abc import ABC

from pygame import Surface

from ..classes.coordinate import Coordinate

class Consumable(ABC):
    """
    Abstract base class to act as a basis for food consumables 
    """

    def __init__(self):
        pass

    def get_consumable_value(self):
        pass

    def get_consumable_name(self):
        pass

    def get_consumable_weight(self):
        pass

    def draw(self, p_game_screen: Surface, p_coordinate: Coordinate):
        pass
