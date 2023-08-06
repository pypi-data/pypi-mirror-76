"""Motor module."""

from enum import IntEnum
from typing import Tuple
from modi.module.output_module.output_module import OutputModule


class Motor(OutputModule):

    class PropertyType(IntEnum):
        FIRST_TORQUE = 2
        SECOND_TORQUE = 10
        FIRST_SPEED = 3
        SECOND_SPEED = 11
        FIRST_DEGREE = 4
        SECOND_DEGREE = 12

    class ControlType(IntEnum):
        TORQUE = 16
        SPEED = 17
        DEGREE = 18
        CHANNEL = 19

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._type = "motor"

    def set_motor_channel(self,
                          motor_channel: int, control_mode: int,
                          control_value: int = None) -> None:
        """Select te motor channel for control
        Mode: 0:Torque 1:Speed 2:Angle (Torque is not implemented yet)

        :param motor_channel: channel number for control 0:Top 1:Bot
        :type motor_channel: int
        :param control_mode: Control mode of the motor to be selected
        :type control_mode: int
        :param control_value: value to control
        :type control_value: int, optional
        :return: current value of the motor control
        :rtype: Tuple[float, float]
        """
        self._set_property(
            self._id,
            self.ControlType.CHANNEL,
            (
                motor_channel,
                control_mode,
                control_value,
                0x00 if control_value >= 0 else 0xFFFF,
            ),
        )

    def set_first_degree(self, degree_value: int) -> int:
        """Sets the angle of the motor at channel I

        :param degree_value: Angle to set the first motor.
        :type degree_value: int, optional
        :return: If *degree* is ``None``, Angle of the first motor.
        :rtype: float, optional
        """
        self.set_degree(first_degree_value=degree_value)
        return degree_value

    def get_first_degree(self) -> float:
        """Returns first degree

        :return: first degree value
        :rtype: float
        """
        return self._get_property(self.PropertyType.FIRST_DEGREE)

    def set_second_degree(self, degree_value: int) -> float:
        """Sets the angle of the motor at channel II

        :param degree_value: Angle to set the second motor.
        :type degree_value
        :return: Angle of the second motor.
        :rtype: float
        """
        self.set_degree(second_degree_value=degree_value)
        return degree_value

    def get_second_degree(self) -> float:
        """Returns second degree

        :return: second degree value
        :rtype: float
        """
        return self._get_property(self.PropertyType.SECOND_DEGREE)

    def set_first_speed(self, speed_value: int) -> float:
        """Set the speed of the motor at channel I

        :param speed_value: Angular speed to set the first motor.
        :return: Angular speed of the first motor.
        :rtype: float
        """
        self.set_speed(first_speed_value=speed_value)
        return speed_value

    def get_first_speed(self) -> float:
        return self._get_property(self.PropertyType.FIRST_SPEED)

    def set_second_speed(self, speed_value: int) -> float:
        """Set the speed of the motor at channel II

        :param speed_value: Angular speed to set the second motor.
        :return: Angular speed of the second motor.
        :rtype: float
        """
        self.set_speed(second_speed_value=speed_value)
        return speed_value

    def get_second_speed(self) -> float:
        return self._get_property(self.PropertyType.SECOND_SPEED)

    def set_first_torque(self, torque_value: int) -> float:
        """Set the torque of the motor at channel I

        :param torque_value: Torque to set the first motor.
        :type torque_value: int
        :return: Torque of the first motor.
        :rtype: float
        """
        self.set_torque(first_torque_value=torque_value)
        return torque_value

    def get_first_torque(self) -> float:
        return self._get_property(self.PropertyType.FIRST_TORQUE)

    def set_second_torque(self, torque_value: int) -> float:
        """Set the torque of the motor at channel II

        :param torque_value: Torque to set the second motor.
        :type torque_value: int
        :return: Torque of the second motor.
        :rtype: float
        """
        self.set_torque(second_torque_value=torque_value)
        return torque_value

    def get_second_torque(self):
        return self._get_property(self.PropertyType.SECOND_TORQUE)

    def set_torque(self, first_torque_value: int = None,
                   second_torque_value: int = None) -> Tuple[float, float]:
        """Set the torque of the motors at both channels

        :param first_torque_value: Torque to set the first motor.
        :type first_torque_value: int, optional
        :param second_torque_value: Torque to set the second motor.
        :type second_torque_value: int, optional
        :return: Torque of the first motor , Torque of the second motor.
        :rtype: Tuple[float, float]
        """
        raise NotImplementedError

        #if first_torque_value is not None:
        #    self.set_motor_channel(0, 0, first_torque_value)
        #if second_torque_value is not None:
        #    self.set_motor_channel(1, 0, second_torque_value)

        #self._update_properties(
        #    [self.PropertyType.FIRST_TORQUE, self.PropertyType.SECOND_TORQUE],
        #    [first_torque_value, second_torque_value])

        #return first_torque_value, second_torque_value

    def get_torque(self) -> Tuple[float, float]:
        """Returns torque values of two motors

        :return: Torque
        :rtype: Tuple[float, float]
        """
        return (
            self._get_property(self.PropertyType.FIRST_TORQUE),
            self._get_property(self.PropertyType.SECOND_TORQUE),
        )

    def set_speed(self, first_speed_value: int = None,
                  second_speed_value: int = None) -> Tuple[float, float]:
        """Set the speed of the motors at both channels

        :param first_speed_value: Speed to set the first motor.
        :type first_speed_value: int, optional
        :param second_speed_value: Speed to set the second motor.
        :type second_speed_value: int, optional
        :return: If *first_speed* is ``None`` and *second_speed* is ``None``,
            Speed of the first motor , Speed of the second motor.
        :rtype: Tuple[float, float]
        """
        if first_speed_value is not None:
            self.set_motor_channel(0, 1, first_speed_value)
        if second_speed_value is not None:
            self.set_motor_channel(1, 1, second_speed_value)

        self._update_properties(
            [self.PropertyType.FIRST_SPEED, self.PropertyType.SECOND_SPEED],
            [first_speed_value, second_speed_value])

        return first_speed_value, second_speed_value

    def get_speed(self):
        return (
            self._get_property(self.PropertyType.FIRST_SPEED),
            self._get_property(self.PropertyType.SECOND_SPEED),
        )

    def set_degree(self, first_degree_value: int = None,
                   second_degree_value: int = None) -> Tuple[float, float]:
        """Set the angle of the motors at both channels

        :param first_degree_value: Angle to set the first motor.
        :type first_degree_value: int, optional
        :param second_degree_value: Angle to set the second motor.
        :type second_degree_value: int, optional
        :return: Angle of the first motor , Angle of the second motor.
        :rtype: Tuple[float, float]
        """
        if first_degree_value is not None:
            self.set_motor_channel(0, 2, first_degree_value)
        if second_degree_value is not None:
            self.set_motor_channel(1, 2, second_degree_value)

        self._update_properties(
            [self.PropertyType.FIRST_DEGREE, self.PropertyType.SECOND_DEGREE],
            [first_degree_value, second_degree_value])

        return first_degree_value, second_degree_value

    def get_degree(self) -> Tuple[float, float]:
        """Returns current angle

        :return: Angle of two motors
        :rtype: float
        """
        return (
            self._get_property(self.PropertyType.FIRST_DEGREE),
            self._get_property(self.PropertyType.SECOND_DEGREE),
        )
