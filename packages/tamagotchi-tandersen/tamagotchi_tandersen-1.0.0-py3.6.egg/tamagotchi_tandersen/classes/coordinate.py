from ..enums.direction import Direction


class Coordinate:
    """
    A class to represent a position on an X/Y screen
    """

    def __init__(self, x_position: int, y_position: int):
        """
        Create a new Coordinate

        Args:
            x_position: The int value representing the position on a x-axis
            y_position: The int value representing the position on a y-axis

        Returns:
            A new Coordinate
        """
        self.x_position = x_position
        self.y_position = y_position
    
    def get_coordinate(self) -> tuple:
        """
        Get a tuple representation of the coordinate object

        Returns:
            Tuple containing the x and y axis positions
        """
        return (self.x_position, self.y_position)

    def get_x(self) -> int:
        """
        Get the x position of the coordinate

        Returns:
            Int representing the position on the x axis
        """
        return self.x_position

    def get_y(self) -> int:
        """
        Get the y position of the coordinate

        Returns:
            Int representing the position on the y axis
        """
        return self.y_position
