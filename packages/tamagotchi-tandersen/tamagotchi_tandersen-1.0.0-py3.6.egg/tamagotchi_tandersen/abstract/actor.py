from abc import ABC

from ..classes.coordinate import Coordinate

class Actor(ABC):
    """
    Abstract base class to act as basis for all actors on the game board
    """
    def __init__(self, p_frames_per_second: int, p_coordinate: Coordinate):
        pass

    def sleep(self):
        pass

    def eat(self):
        pass

    def is_alive(self):
        pass

    def die(self):
        pass

    def get_position(self):
        pass

    def get_health(self):
        pass

    def get_state(self):
        pass

    def get_energy(self):
        pass

    def move(self):
        pass

    def run_turn(self):
        pass

    def draw(self):
        pass
