from pygame import draw, color, Surface
from pygame.locals import Rect

from ..abstract.status_element import StatusElement
from ..abstract.actor import Actor

from .coordinate import Coordinate

class HealthBar(StatusElement):
    """
    Simple status element class to display actor health
    """

    def draw(self, p_game_screen: Surface, p_actor: Actor):
        """
        Draw a health bar on a Surface using the health value of an Actor

        Args:
            p_game_screen: The Surface to draw to
            p_actor: The Actor to display the health value of
        """
        if p_actor.get_health() > 70:
            rectangle = Rect(self.coordinate.get_x(), self.coordinate.get_y(), 60, 20)
            draw.rect(p_game_screen, color.THECOLORS['green'], rectangle)
        elif p_actor.get_health() > 30:
            rectangle = Rect(self.coordinate.get_x(), self.coordinate.get_y(), 60, 20)
            draw.rect(p_game_screen, color.THECOLORS['orange'], rectangle)
        else:
            rectangle = Rect(self.coordinate.get_x(), self.coordinate.get_y(), 60, 20)
            draw.rect(p_game_screen, color.THECOLORS['red'], rectangle)
        
        rectangle_border = Rect(self.coordinate.get_x() - 3, self.coordinate.get_y() - 3, 65, 25)
        draw.rect(p_game_screen, color.THECOLORS['black'], rectangle_border, 2)

        self.draw_header(p_game_screen, "Health")


class EnergyBar(StatusElement):
    """
    Simple status element class to display actor energy
    """

    def draw(self, p_game_screen: Surface, p_actor: Actor):
        """
        Draw an Energy bar on a Surface using the energy value of an Actor

        Args:
            p_game_screen: The Surface to draw to
            p_actor: The Actor to display the energy status of
        """
        if p_actor.get_energy() > 70:
            rectangle = Rect(self.coordinate.get_x(), self.coordinate.get_y(), 60, 20)
            draw.rect(p_game_screen, color.THECOLORS['green'], rectangle)
        elif p_actor.get_energy() > 30:
            rectangle = Rect(self.coordinate.get_x(), self.coordinate.get_y(), 60, 20)
            draw.rect(p_game_screen, color.THECOLORS['orange'], rectangle)
        else:
            rectangle = Rect(self.coordinate.get_x(), self.coordinate.get_y(), 60, 20)
            draw.rect(p_game_screen, color.THECOLORS['red'], rectangle)
        
        rectangle_border = Rect(self.coordinate.get_x() - 3, self.coordinate.get_y() - 3, 65, 25)
        draw.rect(p_game_screen, color.THECOLORS['black'], rectangle_border, 2)

        self.draw_header(p_game_screen, "Energy")