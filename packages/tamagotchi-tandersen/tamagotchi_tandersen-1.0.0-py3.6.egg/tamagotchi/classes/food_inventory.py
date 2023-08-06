from ..abstract.consumable import Consumable

from ..classes.coordinate import Coordinate

from ..enums.direction import Direction

from pygame import draw, color, Surface
from pygame.locals import Rect


class FoodInventory:
    """
    Will contain the available Consumables for use by the actor
    """

    def __init__(self, p_food_list: list, p_coordinate: Coordinate):
        """
        Create a new FoodInventory

        Args:
            p_food_list: The list of food
            p_coordinate: The position for the FoodInventory to display at

        Returns:
            The new FoodInventory
        """
        self.food_list = p_food_list
        self.active_food_index = 0
        self.coordinate = p_coordinate

    def get_available_food(self) -> dict:
        """
        Returns a dictionary of foods available to consume

        Returns:
            A dict with consumable names as keys and occurences in food list as value
        """
        food_occurence_dictionary = {}

        for food in self.food_list:
            if food.get_consumable_name() in food_occurence_dictionary.keys():
                food_occurence_dictionary[food.get_consumable_name()] += 1
            else:
                food_occurence_dictionary[food.get_consumable_name()] = 1

        return food_occurence_dictionary

    def eat_food(self) -> Consumable:
        """
        Eat the current active food

        Returns:
            A Consumable object pop'd from the food_list
        """
        if len(self.food_list) == 0:
            return None
        else:
            tmp_food_index = self.active_food_index
            if self.active_food_index == len(self.food_list) - 1:
                self.active_food_index = 0

            return self.food_list.pop(tmp_food_index)

    def add_food(self, p_food: Consumable):
        """
        Add a food item to the list of available food

        Args:
            p_food: The Consumable to add to the list
        """
        self.food_list.append(p_food)

    def draw(self, p_game_screen: Surface):
        """
        Draws a box showing active food, with quantity with arrows to see the other foods

        Args:
            p_game_screen: The Surface to draw on
        """

        rectangle_size = (50, 50)

        rectangle_border = Rect(self.coordinate.get_coordinate(), rectangle_size)
        draw.rect(p_game_screen, color.THECOLORS['black'], rectangle_border, 5)

        if len(self.food_list) > 1:
            self.draw_arrows(p_game_screen, self.coordinate, rectangle_size)

        if len(self.food_list) > 0:
            self.food_list[self.active_food_index].draw(p_game_screen,
                                                        Coordinate(self.coordinate.get_x() + (rectangle_size[0]/2),
                                                                   self.coordinate.get_y() + (rectangle_size[1]/2))
                                                        )

    def draw_arrows(self, p_game_screen: Surface, p_coordinate: Coordinate, p_rect_size: tuple):
        """
        Internal function for drawing arrows either side of a rectangle

        Args:
            p_game_screen: Surface to draw the arrows to
            p_coordinate: The coordinate to center the arrows off
            p_rect_size: The size of the rectangle they are centered off
        """
        draw.polygon(p_game_screen,
                     color.THECOLORS['black'],
                     (
                        (p_coordinate.get_x() + p_rect_size[0] + 10, p_coordinate.get_y()),
                        (p_coordinate.get_x() + p_rect_size[0] + 30, p_coordinate.get_y() + (p_rect_size[1] / 2)),
                        (p_coordinate.get_x() + p_rect_size[0] + 10, p_coordinate.get_y() + (p_rect_size[1]))
                     )
                    )
        
        draw.polygon(p_game_screen,
                     color.THECOLORS['black'],
                     (
                        (p_coordinate.get_x() - 10, p_coordinate.get_y()),
                        (p_coordinate.get_x() - 30, p_coordinate.get_y() + (p_rect_size[1] / 2)),
                        (p_coordinate.get_x() - 10, p_coordinate.get_y() + (p_rect_size[1]))
                     )
                    )

    def change_active_food(self, direction: Direction):
        """
        Shift the active food to be consumed by giving a direction
        LEFT, DOWN to deincrement
        RIGHT, UP to increment

        Args:
            direction: The direction of the key press
        """
        if direction == Direction.LEFT :
            if self.active_food_index == 0:
                self.active_food_index = len(self.food_list) - 1
            else:
                self.active_food_index -= 1
        elif direction == Direction.RIGHT:
            if self.active_food_index == len(self.food_list) - 1:
                self.active_food_index = 0
            else:
                self.active_food_index += 1
