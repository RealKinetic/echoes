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

from gchaos.settings import DATASTORE_STUB
from gchaos.gae.datastore.actions import ACTIONS
from gchaos.gae.datastore.latency import trigger as trigger_latency
from gchaos.gae.datastore.errors import trigger as trigger_errors


DATSTORE_HOOK_INSTALLED = False


def install_hook(config):
    """Install the datastore hook with binding the datastore config to be
    checked when calls come in.

    Args:
        config (gchaos.config.hydrate.DatastoreConfig):
            Datastore configuration

    Return:
        None
    """
    from google.appengine.api.apiproxy_stub_map import apiproxy

    global DATSTORE_HOOK_INSTALLED

    if DATSTORE_HOOK_INSTALLED:
        return

    apiproxy.GetPreCallHooks().Append(
        'gchaos_datastore_hooks', hook_wrapper(config), DATASTORE_STUB)

    DATSTORE_HOOK_INSTALLED = True


def hook_wrapper(config):
    """The function that wraps all datastore calls. And will trigger the action
    if the service is the datastore stub.

    Args:
        config (gchaos.config.hydrate.{ErrorsConfig|LatenciesConfig|):
            Datastore errors or latencies configuration

    Returns:
        func
    """

    def wrap(service, name, request, response):
        """Called before hitting the datastore stub."""
        assert service == DATASTORE_STUB

        trigger_action(name, config)

    return wrap


def trigger_action(name, config):
    """If the service is a datastore action that we track get the errors or
    latencies for the action from the config and if those exist pass them on to
    the trigger functions.

    Args:
        name (str): Google service action
        config (gchaos.config.hydrate.DatastoreConfig):
            Datastore configuration.

    Return:
        None
    """
    uname = name.upper()

    if uname not in ACTIONS.all():
        logging.info(
            "Action is not in our tracked actions {0}".format(uname))
        return

    _trigger_actions(uname, config)


def _trigger_actions(name, config):
    """Call the trigger functions for errors and latencies.

    Args:
        name (str): Google service action
        config (gchaos.config.hydrate.DatastoreConfig):
            Datastore configuration.

    Return:
        None
    """
    # Errors
    if config.errors.enabled:
        get_config_and_trigger(name, config.errors, trigger_errors)

    # Latencies
    if config.latency.enabled:
        get_config_and_trigger(name, config.latency, trigger_latency)


def get_config_and_trigger(service_name, config, trigger_func):
    """Load the specific configuration from the config for the service. If a
    configuration exists for the service trigger the function passed in with
    that configuration.

    Args:
        service_name (string): Name of the services (should be in ACTIONS)
        config (gchaos.config.hydrate.{ErrorConfig|LatencyConfig}:
            Datastore Configuration
        trigger_func (func): The function to trigger which takes the config

    Return:
        None
    """
    # Load each specific config for the action off errors and latencies
    loaded_config = config.get_by_action(service_name)

    # Trigger the functions for each errors and latencies if the config exists.
    if loaded_config:
        trigger_func(loaded_config)
