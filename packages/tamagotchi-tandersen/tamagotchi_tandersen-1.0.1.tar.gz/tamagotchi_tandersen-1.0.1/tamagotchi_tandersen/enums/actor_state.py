import enum


class ActorState(enum.Enum):
    """
    Enum to represent the states an actor may be in
    """
    AWAKE = "AWAKE"
    ASLEEP = "ASLEEP"
    DEAD = "DEAD"
    POOPING = "POOPING"
    EATING = "EATING"
    WALKING = "WALKING"
