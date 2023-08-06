import unittest

from unittest import mock

from modi.module.output_module.led import Led


class TestLed(unittest.TestCase):
    """Tests for 'Led' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": None}
        self.led = Led(**self.mock_kwargs)

        def eval_set_property(id, command_type, data):
            return command_type

        self.led._set_property = mock.Mock(side_effect=eval_set_property)
        self.led._get_property = mock.Mock()
        self.led._msg_send_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.led

    @mock.patch.object(Led, "set_blue")
    @mock.patch.object(Led, "set_green")
    @mock.patch.object(Led, "set_red")
    def test_set_rgb(self, mock_set_red, mock_set_green, mock_set_blue):
        """Test set_rgb method with user-defined inputs."""
        expected_color = (10, 100, 200)
        self.led.set_rgb(*expected_color)

        expected_rgb_params = (
            self.mock_kwargs["id_"],
            self.led.CommandType.SET_RGB,
            expected_color,
        )
        self.led._set_property.assert_called_once_with(*expected_rgb_params)
        self.assertEqual(self.led._msg_send_q.put.call_count, 3)

    @mock.patch.object(Led, "set_rgb")
    def test_on(self, mock_set_rgb):
        """Test on method."""
        self.led.set_on()

        expected_color = (255, 255, 255)
        mock_set_rgb.assert_called_once_with(*expected_color)

    @mock.patch.object(Led, "set_rgb")
    def test_off(self, mock_set_rgb):
        """Test off method."""
        self.led.set_off()

        expected_color = (0, 0, 0)
        mock_set_rgb.assert_called_once_with(*expected_color)

    @mock.patch.object(Led, "set_rgb")
    def test_set_red(self, mock_set_rgb):
        """Test set_red method."""
        expected_color = self.led.PropertyType.RED
        self.led.set_red(expected_color)
        mock_set_rgb.assert_called_once_with(expected_color, 0, 0)

    def test_get_red(self):
        """Test get_red method with none input."""
        self.led.get_red()
        self.led._get_property.assert_called_once_with(
            self.led.PropertyType.RED)

    @mock.patch.object(Led, "set_rgb")
    def test_set_green(self, mock_set_rgb):
        """Test set_green method."""
        expected_color = self.led.PropertyType.GREEN
        self.led.set_green(green=expected_color)
        mock_set_rgb.assert_called_once_with(0, expected_color, 0)

    def test_get_green(self):
        """Test set_green method with none input."""
        self.led.get_green()
        self.led._get_property.assert_called_once_with(
            self.led.PropertyType.GREEN)

    @mock.patch.object(Led, "set_rgb")
    def test_set_blue(self, mock_set_rgb):
        """Test blue method."""
        expected_color = self.led.PropertyType.BLUE
        self.led.set_blue(blue=expected_color)
        mock_set_rgb.assert_called_once_with(0, 0, expected_color)

    def test_get_blue(self):
        """Test get blue method with none input."""
        self.led.get_blue()
        self.led._get_property.assert_called_once_with(
            self.led.PropertyType.BLUE)


if __name__ == "__main__":
    unittest.main()
