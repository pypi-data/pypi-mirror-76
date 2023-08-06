from ..abstract.actor import Actor
from ..abstract.consumable import Consumable

from .coordinate import Coordinate

from ..enums.actor_state import ActorState
from ..enums.age import Age

from pygame import image, transform, Surface

from pkg_resources import resource_listdir, resource_filename, resource_string

class Pet(Actor):
    """
    The main pet of the game
    """

    def __init__(self, p_frames_per_second: int, p_coordinate: Coordinate):
        """
        Create a new Pet

        Args:
            p_frames_per_second: The frames per second that are run for the game
            p_coordinate: The starting position for the Pet

        Returns:
            The new Pet
        """
        self.energy = 100.0
        self.frames_per_second = p_frames_per_second
        self.age = 0.0
        self.fullness = 0.0
        self.animation_state_max_timer = 0
        self.state_timer = 0
        self.max_health = 100.0
        self.health = self.max_health
        self.position = p_coordinate
        self.state = ActorState.AWAKE

        self.image_width = 100
        self.image_height = 100
        self.image = self.generate_current_image()

    def run_turn(self):
        """
        The actor will operate its turn on the game board
        """
        if self.is_alive():
            self.health -= self.max_health / (60 * self.frames_per_second)  # In 60 seconds the pet will die from lack of nutrition, must factor in frame cycle
            self.age += (100 / (self.frames_per_second * 120))  # In 2 minutes it will get old and die
            self.energy -= 100 / (20 * self.frames_per_second)  # In twenty seconds it will run out of energy and go to sleep
            
            if self.fullness >= 70:
                self.poop()

            if self.state_timer > self.animation_state_max_timer * self.frames_per_second:  # In 3 seconds revert to normal state
                self.awake()
            else:
                self.state_timer += 1

            if self.energy <= 20 and not self.is_doing_action():
                self.sleep()

            if self.health <= 0 or self.age >= 100:
                self.die()

    def is_alive(self) -> bool:
        """
        Returns if the pet is dead

        Returns:
            Boolean representation of the pets alive status
        """
        if self.get_state() == ActorState.DEAD:
            return False
        else:
            return True
    
    def awake(self):
        """
        Set the pet to the awake state
        """
        if self.is_alive():
            self.image = self.generate_current_image()
            self.set_state(ActorState.AWAKE)
    
    def is_doing_action(self) -> bool:
        """
        Check if pet is currently doing an action
        """
        return not self.get_state() == ActorState.AWAKE

    def eat(self, p_consumable: Consumable):
        """
        The pet will eat the food its given to replenish health and increase fullness

        Args:
            p_consumable: A Consumable to be eaten by the Pet
        """
        if self.is_alive():
            if self.health + p_consumable.get_consumable_value() > self.max_health:
                self.health = self.max_health
            else:
                self.health += p_consumable.get_consumable_value()
            
            self.set_state(ActorState.EATING)
            self.fullness += p_consumable.get_consumable_weight()
            self.animation_state_max_timer = 2
            self.state_timer = 0

    def sleep(self):
        """
        The pet will go asleep to regain its energy
        """
        if self.is_alive():
            self.set_state(ActorState.ASLEEP)
            self.energy = 100
            self.state_timer = 0
            self.animation_state_max_timer = 5
            self.image = transform.scale(image.load(
                resource_filename('tamagotchi_tandersen', 'assets/fox-sleeping.png')), (self.image_width, self.image_height))

    def die(self):
        """
        Set the pets state to Dead
        """
        self.set_state(ActorState.DEAD)

    def get_position(self) -> tuple:
        """
        Get the coordinate tuple representation
        """
        return self.position.get_coordinate()
    
    def get_health(self) -> float:
        """
        Get the health of the pet
        """
        return self.health

    def get_state(self) -> ActorState:
        """
        Get the current ActorState of the pet
        """
        return self.state
    
    def get_age(self) -> Age:
        """
        Get an Age state representation of the pets age
        """
        if not self.is_alive():
            return Age.DECEASED
        elif self.age < 13:
            return Age.YOUNG
        elif self.age < 20:
            return Age.TEENAGE
        elif self.age < 65:
            return Age.MIDDLEAGE
        elif self.age <= 100:
            return Age.ELDERLY
        else:
            return Age.DECEASED
    
    def get_energy(self) -> float:
        """
        Get the energy level of the Pet
        """
        return self.energy

    def set_state(self, p_state: ActorState):
        """
        Set the state of the pet

        Args:
            p_state: The ActorState to change the Pet to
        """
        self.state = p_state

    def move(self):
        """
        @TODO add movement and animation to the Pet
        """
        return

    def draw(self, p_game_screen: Surface):
        """
        Draw the current representation of the pet on a Surface

        Args:
            p_game_screen: The Surface to draw the Pet on
        """
        p_game_screen.blit(
                            self.image,
                            (
                                self.position.get_x() - (self.image_width / 2),
                                self.position.get_y() - (self.image_height / 2)
                            )
                        )
    
    def poop(self):
        """
        Clear out the pets full stomach
        """
        if self.is_alive():
            self.set_state(ActorState.POOPING)
            self.fullness = 0
            self.state_timer = 0
            self.animation_state_max_timer = 3

    def generate_current_image(self) -> Surface:
        """
        To visually represent the state of the pet in its age cycle, this will return an image matching its age

        Returns:
            A Surface containing the image to display for the Pet
        """
        current_age = self.get_age()
        
        if current_age == Age.MIDDLEAGE:
            return transform.scale(image.load(
                resource_filename('tamagotchi_tandersen', 'assets/fox-middle.png')), (self.image_width, self.image_height))
        elif current_age == Age.ELDERLY:
            return transform.scale(image.load(
                resource_filename('tamagotchi_tandersen', 'assets/fox-old.png')), (self.image_width, self.image_height))
        elif current_age == Age.DECEASED:
            return transform.scale(image.load(
                resource_filename('tamagotchi_tandersen', 'assets/fox-sleeping.png')), (self.image_width, self.image_height))
        else:
            return transform.scale(image.load(
                resource_filename('tamagotchi_tandersen', 'assets/cute-fox.png')), (self.image_width, self.image_height))
