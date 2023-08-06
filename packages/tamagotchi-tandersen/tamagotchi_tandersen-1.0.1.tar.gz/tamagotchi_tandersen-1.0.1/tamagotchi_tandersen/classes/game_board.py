import pygame

from pygame.surface import Surface

# from . import FoodInventory, Coordinate, Pet

from .pet import Pet
from .food_inventory import FoodInventory
from .coordinate import Coordinate

from ..abstract.actor import Actor
from ..abstract.consumable import Consumable
from ..abstract.status_element import StatusElement

from ..enums.direction import Direction
from ..enums.actor_state import ActorState

from ..factory.consumable_factory import ConsumableFactory
from ..factory.status_bar_factory import StatusBarFactory

class GameBoard:
    """
    The operator and screen of the Tamagotchi challenge game
    """

    def __init__(self, x_length: int, y_length: int):
        """
        Generate a new GameBoard given the size of the screen

        Args:
            x_length: The x dimension size of the scren
            y_length: The y dimension size of the screen

        Returns:
            The new GameBoard
        """
        self.x_length = x_length
        self.y_length = y_length
        self.game_frames_per_second = 30

        self.actor = Pet(self.game_frames_per_second,
                         Coordinate(x_length / 2, y_length / 2)
                        )

        consumable_factory = ConsumableFactory()
        status_bar_factory = StatusBarFactory()

        food_to_create = ["pear", "apple", "strawberry", "pear", "strawberry", "strawberry"]
        food_inventory_list = []
        for food_name in food_to_create:
            try:
                food_inventory_list.append(consumable_factory.get_consumable(food_name))
            except ValueError as e:
                print("ValueError : {} is not an acceptable Consumable name".format(e))

        self.food_inventory = FoodInventory(food_inventory_list, Coordinate(500, 320))

        self.status_bars = [status_bar_factory.get_status_bar("health", Coordinate(40, 350)),
                            status_bar_factory.get_status_bar("energy", Coordinate(120, 350))]

        self.game_over = False
    
    def draw_header(self, p_game_screen: Surface, p_coordinate: Coordinate, p_header: str):
        """
        Draw large text on the game screen at a given coordinate

        Args:
            p_game_screen: The screen to display the text on
            p_coordinate: The coordinate to display the text at
            p_header: The large text to display
        """
        largeText = pygame.font.Font('freesansbold.ttf', 30)
        text_surface = largeText.render(p_header, True, pygame.color.THECOLORS['black'])
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (p_coordinate.get_x(), p_coordinate.get_y())
        p_game_screen.blit(text_surface, text_rectangle)

    def draw_normal_text(self, p_game_screen: Surface, p_coordinate: Coordinate, p_text: str):
        """
        Draw text on the game screen at a given coordinate

        Args:
            p_game_screen: The screen to display the text on
            p_coordinate: The coordinate to display the text at
            p_text: The text to display
        """
        largeText = pygame.font.Font('freesansbold.ttf', 18)
        text_surface = largeText.render(p_text, True, pygame.color.THECOLORS['black'])
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (p_coordinate.get_x(), p_coordinate.get_y())
        p_game_screen.blit(text_surface, text_rectangle)

    def get_actor(self) -> Actor:
        """
        Get the actor run by the game board

        Returns:
            The actor in play
        """
        return self.actor

    def get_board_size(self) -> tuple:
        """
        Get a tuple representation of the size of the game screen

        Returns:
            The tuple of the screen size
        """
        return (self.x_length, self.y_length)

    def get_game_over(self) -> bool:
        """
        Get the state of if the game is over

        Returns:
            The game over boolean
        """
        return self.game_over

    def run_event_queue(self):
        """
        The game loop event handler
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.food_inventory.change_active_food(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.food_inventory.change_active_food(Direction.RIGHT)
                elif event.key == pygame.K_e:
                    if not self.actor.get_state() == ActorState.ASLEEP:
                        food_to_eat = self.food_inventory.eat_food()
                        self.actor.eat(food_to_eat)
                elif event.key == pygame.K_s:
                    self.actor.sleep()
    
    def draw_instructions(self, p_game_screen: Surface):
        """
        Draws the instructions for the player on the Surface

        Args:
            p_game_screen: The Surface to draw the instructions on
        """
        self.draw_header(p_game_screen, Coordinate(self.x_length - 150, 30), "Controls")
        self.draw_normal_text(p_game_screen, Coordinate(self.x_length - 150, 50), "Press e to feed selected food")
        self.draw_normal_text(p_game_screen, Coordinate(self.x_length - 150, 70), "Press s to put pet to sleep")
        self.draw_normal_text(p_game_screen, Coordinate(self.x_length - 150, 90), "Use Left/Right keys to select food")

    def run_game(self):
        """
        Will run the game logic in a loop until the game is exited via closing the game window
        """
        pygame.init()

        screen = pygame.display.set_mode(self.get_board_size())

        pygame.display.set_caption('Tamagotchi Challenge')

        clock = pygame.time.Clock()

        while not self.get_game_over():
            if not self.actor.is_alive():
                break

            self.run_event_queue()

            screen.fill(pygame.color.THECOLORS['white'])
            self.actor.run_turn()
            self.actor.draw(screen)
            self.food_inventory.draw(screen)

            for status_bar in self.status_bars:
                status_bar.draw(screen, self.actor)
            
            self.draw_header(screen, Coordinate(70, 30), self.actor.get_state().value)
            self.draw_instructions(screen)

            pygame.display.update()
            clock.tick(self.game_frames_per_second)

        while not self.get_game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            screen.fill(pygame.color.THECOLORS['white'])
            self.draw_header(screen, Coordinate(self.x_length/2, self.y_length/2 - 50), "Unfortunately, the Pet has died.")
            self.draw_header(screen, Coordinate(self.x_length/2, self.y_length/2), "But thanks for playing!")
            pygame.display.update()
            clock.tick(self.game_frames_per_second)
    
        pygame.quit()
        quit()
