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


from gchaos.choice import Choice
from gchaos.gae.datastore.actions import ACTIONS


DEFAULT_ERROR_ENTRY = ({}, 0.00)
DEFAULT_LATENCY_ENTRY = (None, 0.00)
DEFAULT_CONFIG = (False, {})


class ChaosConfig(object):
    """Chaos configuration object.

    Properties:
        datastore (DatastoreConfig): The datastore configuration
    """

    def __init__(self, config):
        """Initlialize the ChaosConfig object setting the datastore property
        to a DatastoreConfig generated off the passed in config. Defaults to
        empty if not passed in.

        Args:
            config (dict): Dictionary of a Chaos Configuration
        """
        self.datastore = DatastoreConfig(config.get("datastore", {}))


class DatastoreConfig(object):
    """Datastore configuration object.

    Properties:
        enabled (bool): Whether the datastore chaos is enabled
        errors (ErrorsConfig): The datastore errors configuration
        latency (TODO): The datastore latency configuration
    """

    def __init__(self, config):
        """Initlialize the DatastoreConfig object setting the enabled, errors
        and latency properties off the passed in config.

        Args:
            config (dict): Dictionary of a Datastore Configuration
        """
        self.enabled = config.get('enabled', False)
        self.errors = ErrorsConfig(*config.get('errors', DEFAULT_CONFIG))
        self.latency = LatenciesConfig(*config.get('latency', DEFAULT_CONFIG))


class ErrorsConfig(object):
    """Datastore errors configuration object.

    Properties:
        enabled (bool): Flag for enabling
        delete_errors (ErrorConfig): Delete error configuration
        get_errors (ErrorConfig): Get error configuration
        put_errors (ErrorConfig): Put error configuration
    """

    def __init__(self, enabled, config):
        """Initlialize the ErrorsConfig object setting the delete_errors,
        get_errors and put_errors to an ErrorConfig generated off the passed in
        config.

        Args:
            enabled (bool): Flag for enabling
            config (dict): Dictionary of a Datastore Errors Configuration
        """
        self.enabled = enabled
        self.delete_errors = ErrorConfig(
            *config.get("DELETE", DEFAULT_ERROR_ENTRY))
        self.get_errors = ErrorConfig(*config.get("GET", DEFAULT_ERROR_ENTRY))
        self.put_errors = ErrorConfig(*config.get("PUT", DEFAULT_ERROR_ENTRY))
        # self.enabled =

    def get_by_action(self, action):
        """Return the corresponding ErrorConfig for the action passed in.

        Args:
            actions (str): Action as a string. (Options can be found on the
                           ACTIONS global obect.
        """
        if action == ACTIONS.DELETE:
            return self.delete_errors

        elif action == ACTIONS.GET:
            return self.get_errors

        elif action == ACTIONS.PUT:
            return self.put_errors


class ErrorConfig(object):
    """Datastore error configuration object.

    Properties:
        errors (Choice): Choice object of datastore errors
        error_rate (float): Error Rate (should be between 0.00 and 1.00)
    """

    def __init__(self, errors, error_rate):
        """Initialize the ErrorConfig object setting the errors and error_rate
        to the passed in values. The errors are converted to a Choice object.

        Args:
            errors (dict): Dictionary of choices (keys) and propability weights
                           (values)
            error_rate (float): Error rate value between 0.00 and 1.00
        """
        self.errors = Choice(errors.values(), errors.keys())
        self.error_rate = error_rate


class LatenciesConfig(object):
    """Datastore latencies configuration object.

    Properties:
        enabled (bool): Flag for enabling
        delete_latencies (LatencyConfig): Delete latency configuration
        get_latencies (LatencyConfig): Get latency configuration
        put_latencies (LatencyConfig): Put latency configuration
    """

    def __init__(self, enabled, config):
        """Initlialize the LatenciesConfig object setting the delete_latencies,
        get_latencies and put_latencies to a LatencyConfig generated off the
        passed in config.

        Args:
            enabled (bool): Flag for enabling
            config (dict): Dictionary of a Datastore Latencies Configuration
        """
        self.enabled = enabled

        self.delete_latencies = LatencyConfig(
            *config.get("DELETE", DEFAULT_LATENCY_ENTRY))

        self.get_latencies = LatencyConfig(
            *config.get("GET", DEFAULT_LATENCY_ENTRY))

        self.put_latencies = LatencyConfig(
            *config.get("PUT", DEFAULT_LATENCY_ENTRY))

    def get_by_action(self, action):
        """Return the corresponding LatencyConfig for the action passed in.

        Args:
            actions (str): Action as a string. (Options can be found on the
                           ACTIONS global obect.
        """
        if action == ACTIONS.DELETE:
            return self.delete_latencies

        elif action == ACTIONS.GET:
            return self.get_latencies

        elif action == ACTIONS.PUT:
            return self.put_latencies


class LatencyConfig(object):
    """Datastore latency configuration object.

    Properties:
        latencies (Choice): Choice object of datastore latencies
        latency_rate (float): Latency Rate (should be between 0.00 and 1.00)
    """

    def __init__(self, latency, latency_rate):
        """Initialize the LatencyConfig object setting the latencies and
        latency_rate to the passed in values. The latencies are converted to a
        Choice object.

        Args:
            latency (tuple): A tuple that is the range of a latency spike to
                             pic from. The second value can be ignored to just
                             use a constant rate.
            latency_rate (float): Latency rate value between 0.00 and 1.00
        """
        self.latency = latency
        self.latency_rate = latency_rate
