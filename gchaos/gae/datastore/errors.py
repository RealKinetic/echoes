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

from gchaos.chance import roll
from gchaos.errors import ChaosException
from gchaos.utils import get_func_info_for_path


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
    if not roll(error_config.error_rate):
        return

    if error_config.errors.choices and error_config.errors.weights:
        logging.info("Looking for error to raise.")
        error_info = get_func_info_for_path(error_config.errors.next())
        logging.info("Going to raise %s", error_info.name)
        raise error_info.func()

    raise ChaosException("Raising Chaos!")
