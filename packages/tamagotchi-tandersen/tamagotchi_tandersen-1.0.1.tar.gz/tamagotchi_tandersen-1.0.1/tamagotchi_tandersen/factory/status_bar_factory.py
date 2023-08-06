from ..abstract.status_element import StatusElement

from ..classes.state_bars import HealthBar, EnergyBar
from ..classes.coordinate import Coordinate


class StatusBarFactory:
    """
    A factory for generating StatusElements
    """

    def get_status_bar(self, p_status_type: str, p_coordinate: Coordinate) -> StatusElement:
        """
        Factory function for generating new status bars given the status bar name

        Args:
            p_status_type: A name that matches the name of a StatusElement
            p_coordinate: The position for the status bar

        Returns:
            The new StatusElement

        Raises:
            ValueError: If no class name matches the p_status_type
        """
        if p_status_type.lower() == "health":
            return HealthBar(p_coordinate)
        elif p_status_type.lower() == "energy":
            return EnergyBar(p_coordinate)
        else:
            raise ValueError(p_status_type)
