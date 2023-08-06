from ..abstract.consumable import Consumable

from ..classes.food import Pear, Apple, Strawberry

class ConsumableFactory:
    """
    A factory for generating Consumables
    """

    def get_consumable(self, p_consumable_name: str) -> Consumable:
        """
        Factory function for generating new consumables given the consumable name

        Args:
            p_consumable_name: A name that matches the name of a Consumable

        Returns:
            The new consumable

        Raises:
            ValueError: If no class name matches the p_consumable_name
        """
        if p_consumable_name.lower() == "pear":
            return Pear()
        elif p_consumable_name.lower() == "apple":
            return Apple()
        elif p_consumable_name.lower() == "strawberry":
            return Strawberry()
        else:
            raise ValueError(p_consumable_name)
