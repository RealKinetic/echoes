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


import bisect
from random import random


class Choice(object):
    """Class to hold choices and their corresponding propability weights. It
    caches the accumulated weights as totals which are used to pull from.
    """

    def __init__(self, weights, choices):
        """Initializes the Choice object. Setting the weights and choices to
        the passed in values. Initializes totals to None.

        Args:
            weights (list<int>): List of weights as integers that correspond
                                 to the choices
            choices (list<string>): List of the choices as strings that correspond
                                    to the weights
        """
        self.weights = weights
        self.choices = choices
        self.totals = None

    def next(self):
        """Returns a choice based off the weights and choices passed in.

        Return:
            Choice (string): The choice based off the weight distribution.
        """
        if not (self.weights and self.choices):
            return

        if not self.totals:
            self.totals = fold_weights(self.weights)

        return weighted_choice(self.totals, self.choices)


def weighted_choice(totals, choices):
    """Returns a choice based off the totals and choices passed in.

    Args:
        totals (list<int>): List of totalled weights as integers that correspond
                            to the choices
        choices (list<string>): List of the choices as strings that correspond
                                to the weights

    Return:
        Choice (string): The choice based off the weight distribution.
    """
    rnd = random() * totals[-1]

    return choices[bisect.bisect_right(totals, rnd)]


def fold_weights(weights):
    """Return a list of the weights where we add the weight to the sum of the
    previous weights in the list.

    NOTE: In python 3 we could use itertools.accumulate

    Args:
        weights (list<int>): List of weights as integers that correspond to the
                             choices

    Return:
        folded weights (list<int>)
    """
    accum = 0
    totals = []

    for w in weights:
        accum += w
        totals.append(accum)

    return totals
