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

from mock import MagicMock
from mock import patch

from gchaos.config import CHAOS_CONFIG
from gchaos.config.hydrate import LatencyConfig
from gchaos.errors import InvalidLatencyException

from gchaos.gae.datastore.actions import ACTIONS
from gchaos.gae.datastore.latency import get_stall_time_from_range
from gchaos.gae.datastore.latency import stall
from gchaos.gae.datastore.latency import _stall
from gchaos.gae.datastore.latency import trigger


@patch('gchaos.gae.datastore.latency.roll')
class TriggerTestCase(unittest.TestCase):

    @patch('gchaos.gae.datastore.latency.stall')
    def test_latency_rate_less_than_chance(self, stall, roll):
        """Ensure when the chance is greater than the latency rate that the
        stall method is not called.
        """
        roll.return_value = False

        config = LatencyConfig(None, 0.01)

        trigger(config)

        roll.assert_called_once_with(0.01)
        stall.assert_not_called()


@patch('gchaos.gae.datastore.latency._stall')
class StallTestCase(unittest.TestCase):

    def test_latency_not_configured(self, _stall_mock):
        """Ensure when no latency is set on the config that no other actions
        are triggered.
        """
        stall(None)

        _stall_mock.assert_not_called()

    def test_latency_configured_with_single_value(self, _stall_mock):
        """Ensure when a single value latency is set on the config that the
        _stall function is called with that.
        """
        stall((1000,))

        _stall_mock.assert_called_once_with(1000)

    def test_latency_configured_with_int_value(self, _stall_mock):
        """Ensure when a single int value latency is set on the config that the
        _stall function is called with that.
        """
        stall(1000)

        _stall_mock.assert_called_once_with(1000)

    def test_latency_configured_with_bad_value(self, _stall_mock):
        """Ensure when a bad latency value is set on the config that an
        InvalidLatencyException is raised.
        """
        self.assertRaises(InvalidLatencyException, stall, "a")

        _stall_mock.assert_not_called()

    @patch('gchaos.gae.datastore.latency.get_stall_time_from_range')
    def test_latency_configured_with_rage(self, range_mock, _stall_mock):
        """Ensure when a range latency is set on the config that the _stall
        function is called with the result of getting the value from the range.
        """
        range_mock.return_value = 2000

        stall((1000, 3000))

        _stall_mock.assert_called_once_with(2000)
        range_mock.assert_called_once_with((1000, 3000))


class GetStallTimeFromRangeTestCase(unittest.TestCase):

    def test_latency_not_a_2_value_tuple(self):
        """Ensure if latency is not a 2 value tuple that an
        InvalidLatencyException is raised.
        """
        self.assertRaises(
            InvalidLatencyException, get_stall_time_from_range, (1, 2, 3))

    def test_latency_2nd_value_not_greater_than_first_value(self):
        """Ensure if the latency tuple has a second value less than the first
        that an InvalidLatencyException is raised.
        """
        self.assertRaises(
            InvalidLatencyException, get_stall_time_from_range, (3, 2))

    @patch('gchaos.gae.datastore.latency.randint')
    def test_latency_is_valid(self, randint):
        """Ensure if the latency is valid that it calls into randint and returns
        it's result.
        """
        randint.return_value = 2000

        result = get_stall_time_from_range((1000, 3000))

        self.assertEqual(result, 2000)

        randint.assert_called_once_with(1000, 3000)


class StallSleepTestCase(unittest.TestCase):

    @patch('gchaos.gae.datastore.latency.sleep')
    def test_stall(self, sleep):
        """Ensure sleep is called with the correct value."""
        _stall(1500)

        sleep.assert_called_once_with(1.5)
