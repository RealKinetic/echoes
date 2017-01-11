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

from google.appengine.api import datastore_errors

from mock import MagicMock
from mock import patch

from gchaos.config import CHAOS_CONFIG
from gchaos.config.hydrate import ErrorConfig
from gchaos.errors import ChaosException
from gchaos.gae.datastore.actions import ACTIONS
from gchaos.utils import full_name

from gchaos.gae.datastore.errors import trigger
from gchaos.gae.datastore.errors import trigger_action_error


class TriggerActionErrorTests(unittest.TestCase):

    def test_name_not_in_actions(self):
        """Ensure if the name is not in the actions that no subsequent calls
        are made.
        """
        name = "foo"

        error_config = CHAOS_CONFIG.datastore.errors
        error_config.get_by_action = MagicMock(return_value=None)

        trigger_action_error(name, error_config)

        error_config.get_by_action.assert_not_called()

    @patch('gchaos.gae.datastore.errors.trigger')
    def test_name_in_actions_but_no_error_config(self, trigger_mock):
        """Ensure if the name is in the actions it loads the error config but
        since that's None it doesn't trigger.
        """
        name = ACTIONS.GET

        error_config = CHAOS_CONFIG.datastore.errors
        error_config.get_by_action = MagicMock(return_value=None)

        trigger_action_error(name, error_config)

        error_config.get_by_action.assert_called_once_with(name)
        trigger_mock.assert_not_called()

    @patch('gchaos.gae.datastore.errors.trigger')
    def test_name_in_actions_and_has_error_config(self, trigger_mock):
        """Ensure if the name is in the actions it loads the error config and
        since that returns a config it calls trigger with the config.
        """
        name = ACTIONS.PUT

        put_config = CHAOS_CONFIG.datastore.errors.put_errors

        error_config = CHAOS_CONFIG.datastore.errors
        error_config.get_by_action = MagicMock(return_value=put_config)

        trigger_action_error(name, error_config)

        error_config.get_by_action.assert_called_once_with(name)
        trigger_mock.assert_called_once_with(put_config)


@patch('gchaos.gae.datastore.errors._get_chance')
class TriggerTestCase(unittest.TestCase):

    def test_error_rate_less_than_chance(self, chance):
        """Ensure when the chance is greater than the error rate that no
        execption is raised.
        """
        chance.return_value = 1

        config = ErrorConfig({"a": 1}, 0.01)

        trigger(config)

        chance.assert_called_once_with()

    def test_error_rate_greater_than_chance_but_no_errors(self, chance):
        """Ensure when the error rate is greater than the chance but there are
        no errors configured that a ChaosException is raised.
        """
        chance.return_value = 0

        config = ErrorConfig({}, 1)

        self.assertRaises(ChaosException, trigger, config)

        chance.assert_called_once_with()

    def test_error_rate_greater_than_chance_with_errors(self, chance):
        """Ensure when the error rate is greater than the chance and there are
        errors configured that an Exception from the errors Choice is raised.
        """
        chance.return_value = 0

        err = full_name(datastore_errors.BadValueError)
        config = ErrorConfig({err: 1}, 1)

        self.assertRaises(datastore_errors.BadValueError, trigger, config)

        chance.assert_called_once_with()
