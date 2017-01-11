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


import logging

from collections import defaultdict
import random


from itertools import ifilter
from itertools import imap

from gchaos.errors import ChaosException
from gchaos.gae.datastore.actions import ACTIONS
from gchaos.settings import DATASTORE_STUB
from gchaos.utils import get_func_info_for_path


INSTALLED = False


def install_error_hook(config):
    """Install the datastore errors hook with binding the config to be checked
    when calls come in.

    Args:
        config (gchaos.config.hydrate.ErrorsConfig):
            Datastore errors configuration

    Return:
        None
    """
    from google.appengine.api.apiproxy_stub_map import apiproxy

    global INSTALLED

    if INSTALLED:
        return

    apiproxy.GetPreCallHooks().Append(
        'gchaos_datastore_errors', error_check_config(config),
        DATASTORE_STUB)

    INSTALLED = True


def error_check_config(errors_config):
    """The function that wraps all datastore calls. And will trigger the action
    if the service is the datastore stub.

    Args:
        errors_config (gchaos.config.hydrate.ErrorsConfig):
            Datastore errors configuration

    Returns:
        func
    """

    def error_check(service, name, request, response):
        """Called before hitting the datastore stub."""
        assert service == DATASTORE_STUB

        trigger_action_error(name, errors_config)

    return error_check


def trigger_action_error(name, errors_config):
    """If the service is a datastore action that we track get the errors for
    the action from the config and if those exist pass them on to the trigger
    function.

    Args:
        name (str): Google service action
        errors_config (gchaos.config.hydrate.ErrorsConfig):
            Datastore errors configuration.

    Return:
        None
    """
    uname = name.upper()

    if uname not in ACTIONS.all():
        logging.info(
            "Action is not in our tracked actions {0}".format(uname))
        return

    error_config = errors_config.get_by_action(uname)

    if error_config:
        trigger(error_config)


def trigger(error_config):
    """Generates a chance value between 0 and 1. If the error rate on the error
    config is greather than or equal to the chance then it will trigger errors
    if errors exist on the config. It will get the error configs next option
    which is based on the error config probabilities.

    Args:
        error_config (gchaos.config.hydrate.ErrorConfig): Datastore Error
                                                          Configuration

    Return:
        None
    """
    chance = _get_chance()

    logging.info("ERROR RATE {0} AND CHANCE {1}".format(
        error_config.error_rate, chance))

    if error_config.error_rate < chance:
        # TODO: Look at using inspect to insert this definition will always
        # work.
        return

    if error_config.errors.choices and error_config.errors.weights:
        logging.info("Looking for error to raise.")
        error_info = get_func_info_for_path(error_config.errors.next())
        logging.info("Going to raise %s", error_info.name)
        raise error_info.func()

    raise ChaosException("Raising Chaos!")


def _get_chance():
    """Generate a random number and return it.

    Return:
        int
    """
    random.seed()
    return random.random()
