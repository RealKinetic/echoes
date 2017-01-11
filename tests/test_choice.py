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

from nose.plugins.attrib import attr

from gchaos.choice import Choice


class TestChoice(unittest.TestCase):

    def test_no_weights(self):
        """Ensure if no weights are passed in return None."""
        result = Choice([], ["a"]).next()

        self.assertIsNone(result)

    def test_no_choices(self):
        """Ensure if no choices are passed in return None."""
        result = Choice([5], []).next()

        self.assertIsNone(result)

    def test_single_choice_with_a_weight_of_100(self):
        """Ensure if a single choice is passed in with a chance of 100 that
        choice is returned.
        """
        choice = "mychoice"
        result = Choice([100], [choice]).next()

        self.assertEqual(result, choice)


@attr('slow')
class TestChoiceSlow(unittest.TestCase):

    def test_multiple_choices_with_weights_of_50(self):
        """Ensure if a single choice is passed in with a chance of 100 that
        choice is returned.

        NOTE: This can be slow due to the hacky loop.
        """
        choices = ["mychoice", "mychoice2"]

        done = {}

        for _ in xrange(1000):
            result = Choice([50, 50], choices).next()

            self.assertIn(result, choices)

            done[result] = True

            if len(done) == 2:
                return

        print done
        raise Exception("Never hit 2 choices. This really shouldn't happen.")
