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

import random
from random import randint
from time import sleep

from gchaos.chance import roll
from gchaos.errors import InvalidLatencyException
from gchaos.utils import get_func_info_for_path


def trigger(latency_config):
    """Generates a chance value between 0 and 1. If the latency rate on the
    latency config is greather than or equal to the chance then it will trigger
    latencies if latencies exist on the config. It will get the latency configs
    next option which is based on the latency config probabilities.

    Args:
        latency_config (gchaos.config.hydrate.LatncyConfig):
            Datastore Latency Configuration

    Return:
        None
    """
    if not roll(latency_config.latency_rate):
        return

    stall(latency_config.latency)


def stall(latency):
    """Based off the latency stall for that long. The latency is a tuple if only
    one value is provided then stall for exactly that long. If to values are
    provided then stall for a random choice between those values.

    Args:
        latency (tuple(int, int): A tuple of a latency range (in milliseconds)

    Return:
        None
    """
    if not latency:
        return

    _stall(_get_latency(latency))


def _get_latency(latency):
    """Check the latency field and if it's a single value tuple or an integer
    then return that value. If it's a 2 value tuple then get the value from the
    range. Otherwise raise an InvalidLatencyException.

    Args:
        latency (tuple(int,) | tuple(int, int) | int):
            A tuple of one or two ints or just an int.

    Return:
        None
    """
    if isinstance(latency, tuple):
        if len(latency) == 1:
            return latency[0]

        return get_stall_time_from_range(latency)

    if isinstance(latency, int):
        return latency

    raise InvalidLatencyException(latency)


def get_stall_time_from_range(latency):
    """Take the latency tuple and randomly choose a value that falls within
    that range.

    Args:
        latency (tuple(int, int)): A tuple of ints to make a range

    Return:
        int
    """
    if len(latency) != 2:
        raise InvalidLatencyException(latency)

    min_, max_ = latency

    if max_ < min_:
        raise InvalidLatencyException(latency)

    random.seed()
    # TODO: Ensure second value is greater
    return randint(min_, max_)


def _stall(milli_time):
    """Call time.sleep with the time (in milliseconds) divided by 1000 to
    convert it to seconds.

    Args:
        milli_time (int): Time in milliseconds

    Return:
        None
    """
    logging.info(
        "CHAOS: Starting to stall the call for {0} milliseconds".format(
            milli_time))

    sleep(milli_time / float(1000))
