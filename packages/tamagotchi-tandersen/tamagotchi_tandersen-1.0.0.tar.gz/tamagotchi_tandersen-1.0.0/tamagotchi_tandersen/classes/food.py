from ..abstract.consumable import Consumable

from .coordinate import Coordinate

from pygame import image, transform, Surface

from pkg_resources import resource_filename

class Pear(Consumable):
    """
    A Pear Consumable
    """

    def __init__(self):
        """
        Create a new Pear

        Returns:
            A new Pear
        """
        self.image_width = 30
        self.image_height = 30

        image_to_use = image.load(resource_filename('tamagotchi_tandersen', 'assets/pixel-pear.png'))
        self.image = transform.scale(image_to_use, (self.image_width, self.image_height))

    def get_consumable_value(self) -> int:
        """
        Get the value of the Pear

        Returns:
            The integer value of the Pear
        """
        return 40

    def get_consumable_name(self) -> str:
        """
        Get string representation of the Pear

        Returns:
            The string of Pear
        """
        return "Pear"
    
    def get_consumable_weight(self) -> int:
        """
        Get the weight of the Pear

        Returns:
            Weight of a Pear
        """
        return 50

    def draw(self, p_game_screen: Surface, p_coordinate: Coordinate):
        """
        Draw the Pear on a Surface given a Coordinate
        """
        p_game_screen.blit(
                            self.image,
                            (
                                p_coordinate.get_x() - (self.image_width / 2),
                                p_coordinate.get_y() - (self.image_height / 2)
                            )
                        )


class Apple(Consumable):
    """
    An Apple Consumable
    """

    def __init__(self):
        """
        Create a new Apple

        Returns:
            A new Apple
        """
        self.image_width = 30
        self.image_height = 30

        image_to_use = image.load(resource_filename('tamagotchi_tandersen', 'assets/pixel-apple.jpg'))
        self.image = transform.scale(image_to_use, (self.image_width, self.image_height))

    def get_consumable_value(self) -> int:
        """
        Get the value of the Apple

        Returns:
            The integer value of the Apple
        """
        return 60

    def get_consumable_name(self) -> str:
        """
        Get string representation of the Apple

        Returns:
            The string of Apple
        """
        return "Apple"

    def get_consumable_weight(self) -> int:
        """
        Get the weight of the Apple

        Returns:
            Weight of a Apple
        """
        return 70
    
    def draw(self, p_game_screen: Surface, p_coordinate: Coordinate):
        """
        Draw an Apple on a surface given a Coordinate
        """
        p_game_screen.blit(
                            self.image,
                            (
                                p_coordinate.get_x() - (self.image_width / 2),
                                p_coordinate.get_y() - (self.image_height / 2)
                            )
                        )


class Strawberry(Consumable):
    """
    A Strawberry consumable
    """

    def __init__(self):
        """
        Create a new Strawberry

        Returns:
            A new Strawberry
        """
        self.image_width = 30
        self.image_height = 30

        image_to_use = image.load(resource_filename('tamagotchi_tandersen', 'assets/pixel-strawberry.jpg'))
        self.image = transform.scale(image_to_use, (self.image_width, self.image_height))

    def get_consumable_value(self) -> int:
        """
        Get the value of the Strawberry

        Returns:
            The integer value of the Strawberry
        """
        return 20
    
    def get_consumable_name(self) -> str:
        """
        Get string representation of the Strawberry

        Returns:
            The string of Strawberry
        """
        return "Strawberry"

    def get_consumable_weight(self) -> int:
        """
        The weight value of the Strawberry

        Returns:
            Weight of a Strawberry
        """
        return 30
    
    def draw(self, p_game_screen: Surface, p_coordinate: Coordinate):
        """
        Draw the Strawberry on a Surface given a Coordinate
        """
        p_game_screen.blit(
                            self.image,
                            (
                                p_coordinate.get_x() - (self.image_width / 2),
                                p_coordinate.get_y() - (self.image_height / 2)
                            )
                        )
