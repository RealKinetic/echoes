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
        self.errors = ErrorsConfig(config.get('errors', {}))
        self.latency = None


class ErrorsConfig(object):
    """Datastore errors configuration object.

    Properties:
        delete_errors (ErrorConfig): Delete error configuration
        get_errors (ErrorConfig): Get error configuration
        put_errors (ErrorConfig): Put error configuration
    """

    def __init__(self, config):
        """Initlialize the ErrorsConfig object setting the delete_errors,
        get_errors and put_errors to an ErrorConfig generated off the passed in
        config.

        Args:
            config (dict): Dictionary of a Datastore Errors Configuration
        """
        self.delete_errors = ErrorConfig(
            *config.get("DELETE", DEFAULT_ERROR_ENTRY))
        self.get_errors = ErrorConfig(*config.get("GET", DEFAULT_ERROR_ENTRY))
        self.put_errors = ErrorConfig(*config.get("PUT", DEFAULT_ERROR_ENTRY))

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
