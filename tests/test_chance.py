# MIT License

# Copyright (c) 2017 Real Kinetic

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import unittest

from mock import patch

from gchaos.chance import roll


@patch('gchaos.chance._get_chance')
class RollTestCase(unittest.TestCase):

    def test_value_is_less_than_chance(self, get_chance_mock):
        """Ensure if the value is less than the chance that it returns false."""
        get_chance_mock.return_value = 0.99
        value = 0.01

        result = roll(value)

        self.assertFalse(result)

        get_chance_mock.assert_called_once_with()

    def test_value_is_greater_than_chance(self, get_chance_mock):
        """Ensure if the value is greater than the chance that it returns true."""
        get_chance_mock.return_value = 0.01
        value = 0.99

        result = roll(value)

        self.assertTrue(result)

        get_chance_mock.assert_called_once_with()

    def test_value_is_equal_to_chance(self, get_chance_mock):
        """Ensure if the value is equal to the chance that it returns true."""
        get_chance_mock.return_value = 0.50
        value = 0.50

        result = roll(value)

        self.assertTrue(result)

        get_chance_mock.assert_called_once_with()
