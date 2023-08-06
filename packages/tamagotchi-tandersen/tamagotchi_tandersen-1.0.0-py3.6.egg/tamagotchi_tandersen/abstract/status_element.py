from abc import ABC
from pygame import color, font
from pygame.surface import Surface

from .actor import Actor

from ..classes.coordinate import Coordinate

class StatusElement(ABC):
    """
    Abstract base class to act as a basis for drawable screen elements
    """
    def __init__(self, p_coordinate: Coordinate):
        """

        """
        self.coordinate = p_coordinate

    def draw(self, p_game_screen: Surface, p_actor: Actor):
        pass

    def draw_header(self, p_game_screen: Surface, p_header: str):
        """
        Draws a header text over the Status elements Coordinate
        """
        largeText = font.Font('freesansbold.ttf',18)
        text_surface = largeText.render(p_header, True, color.THECOLORS['black'])
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.coordinate.get_x() + 25, self.coordinate.get_y() - 20)
        p_game_screen.blit(text_surface, text_rectangle)