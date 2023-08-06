"""Led module."""

from enum import IntEnum
from typing import Tuple
from modi.module.output_module.output_module import OutputModule


class Led(OutputModule):

    class PropertyType(IntEnum):
        RED = 2
        GREEN = 3
        BLUE = 4

    class CommandType(IntEnum):
        SET_RGB = 16

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._type = "led"

    def set_rgb(self, red: int = 0, green: int = 0,
                blue: int = 0) -> Tuple[float, float, float]:
        """Sets the color of the LED light with given RGB values, and returns
        the current RGB values.

        :param red: Red component to set or ``None``.
        :type red: int, optional
        :param green: Green component to set or ``None``.
        :type green: int, optional
        :param blue: Blue component to set or ``None``.
        :type blue: int, optional
        :return: Tuple of red, green
        :rtype: Tuple[float, float, float]
        """
        color = (red, green, blue)
        self._set_property(
            self._id,
            self.CommandType.SET_RGB,
            color,
        )
        self._update_properties([property_type
                                 for property_type in self.PropertyType],
                                color)
        return color

    def set_on(self) -> Tuple[float, float, float]:
        """Turn on led at maximum brightness.

        :return: RGB value of the LED set to maximum brightness
        :rtype: Tuple[float, float, float]
        """
        return self.set_rgb(255, 255, 255)

    def set_off(self) -> Tuple[float, float, float]:
        """Turn off led.

        :return: RGB value of the LED turned off
        :rtype: Tuple[float, float, float]
        """
        return self.set_rgb(0, 0, 0)

    def set_red(self, red: int = 255) -> float:
        """Sets the red component of the LED light by given value

        :param red: Red component to set or ``None``.
        :type red: int, optional
        :return: If *red* is ``None``. Red component.
        :rtype: float
        """
        self.set_rgb(red, 0, 0)
        return red

    def get_red(self) -> float:
        """Returns the current value of the red component of the LED

        :return: Red component
        :rtype: float
        """
        return self._get_property(self.PropertyType.RED)

    def set_green(self, green: int = 255) -> float:
        """Sets the green component of the LED light by given value

        :param green: Green component to set
        :type green: int, optional
        :return: Green component.
        :rtype: float
        """
        self.set_rgb(0, green, 0)
        return green

    def get_green(self) -> float:
        """Returns the current value of the green component of the LED

        :return: Green component
        :rtype: float
        """
        return self._get_property(self.PropertyType.GREEN)

    def set_blue(self, blue: int = 255) -> float:
        """Sets the blue component of the LED light by given value

        :param blue: Blue component to set
        :type blue: int, optional
        :return: Blue component.
        :rtype: float
        """
        self.set_rgb(0, 0, blue)
        return blue

    def get_blue(self) -> float:
        """Returns the current value of the blue component of the LED

        :return: Blue component
        :rtype: float
        """
        return self._get_property(self.PropertyType.BLUE)
