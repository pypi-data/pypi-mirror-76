"""Display module."""

from enum import IntEnum

from modi.module.output_module.output_module import OutputModule


class Display(OutputModule):

    class PropertyType(IntEnum):
        TEXT = 17
        CLEAR = 21
        VARIABLE = 22

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._type = "display"

    def set_text(self, text: str) -> str:
        """Clears the display and show the input string on the display.
        Returns the json serialized signal sent to the module
        to display the text

        :param text: Text to display.
        :type text: string
        :return: A json serialized signal to module
        :rtype: string
        """
        self.clear()
        self._set_property(
            self._id,
            self.PropertyType.TEXT,
            text,
            self.PropertyDataType.STRING
        )
        return text

    def set_variable(self, variable: float, position_x: int,
                     position_y: int) -> None:
        """Clears the display and show the input variable on the display.
        Returns the json serialized signal sent to
        the module to display the text

        :param variable: variable to display.
        :type variable: float
        :param position_x: x coordinate of the desired position
        :type position_x: int
        :param position_y: y coordinate of te desired position
        :type position_y: int
        :return: A json serialized signal to module
        :rtype: string
        """
        self._set_property(
            self._id,
            self.PropertyType.VARIABLE,
            (variable, position_x, position_y),
            self.PropertyDataType.DISPLAY_VAR,
        )

    def clear(self) -> None:
        """Clear the screen.

        :return: json serialized message to te module
        :rtype: string
        """
        self._set_property(
            self._id,
            self.PropertyType.CLEAR,
            bytes(2),
            self.PropertyDataType.RAW
        )
