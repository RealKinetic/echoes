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

from gchaos.config import DEFAULT_CONFIG
from gchaos.config.datastore import CONFIG as DS_CONFIG
from gchaos.config.hydrate import ChaosConfig
from gchaos.config.hydrate import DatastoreConfig


class HydrateChaosConfigTests(unittest.TestCase):

    def test_default_config(self):
        """Ensure the default config hydrates correctly."""
        result = ChaosConfig(DEFAULT_CONFIG)

        self.assertIsNotNone(result.datastore)

        verify_datastore_config(result.datastore, self)


class HydrateDataStoreConfigTests(unittest.TestCase):

    def test_default_config(self):
        """Ensure the default config hydrates correctly."""
        result = DatastoreConfig(DS_CONFIG)

        verify_datastore_config(result, self)


def verify_datastore_config(datastore_config, runner):
    runner.assertEqual(datastore_config.enabled, True)

    # DELETE ERRORS
    runner.assertEqual(datastore_config.errors.delete_errors.error_rate, 0.05)
    runner.assertEqual(
        datastore_config.errors.delete_errors.errors.choices,
        DS_CONFIG["errors"]["DELETE"][0].keys()
    )
    runner.assertEqual(
        datastore_config.errors.delete_errors.errors.weights,
        DS_CONFIG["errors"]["DELETE"][0].values()
    )

    # GET ERRORS
    runner.assertEqual(datastore_config.errors.get_errors.error_rate, 0.01)
    runner.assertEqual(
        datastore_config.errors.get_errors.errors.choices,
        DS_CONFIG["errors"]["GET"][0].keys()
    )
    runner.assertEqual(
        datastore_config.errors.get_errors.errors.weights,
        DS_CONFIG["errors"]["GET"][0].values()
    )

    # PUT ERRORS
    runner.assertEqual(datastore_config.errors.put_errors.error_rate, 0.02)
    runner.assertEqual(
        datastore_config.errors.put_errors.errors.choices,
        DS_CONFIG["errors"]["PUT"][0].keys()
    )
    runner.assertEqual(
        datastore_config.errors.put_errors.errors.weights,
        DS_CONFIG["errors"]["PUT"][0].values()
    )

    # DELETE LATENCIES
    runner.assertEqual(datastore_config.latency.delete_latencies.latency_rate,
                       0.05)
    runner.assertEqual(
        datastore_config.latency.delete_latencies.latencies.choices,
        DS_CONFIG["latency"]["DELETE"][0].keys()
    )
    runner.assertEqual(
        datastore_config.latency.delete_latencies.latencies.weights,
        DS_CONFIG["latency"]["DELETE"][0].values()
    )

    # GET LATENCIES
    runner.assertEqual(datastore_config.latency.get_latencies.latency_rate,
                       0.01)
    runner.assertEqual(
        datastore_config.latency.get_latencies.latencies.choices,
        DS_CONFIG["latency"]["GET"][0].keys()
    )
    runner.assertEqual(
        datastore_config.latency.get_latencies.latencies.weights,
        DS_CONFIG["latency"]["GET"][0].values()
    )

    # PUT LATENCIES
    runner.assertEqual(datastore_config.latency.put_latencies.latency_rate,
                       0.02)
    runner.assertEqual(
        datastore_config.latency.put_latencies.latencies.choices,
        DS_CONFIG["latency"]["PUT"][0].keys()
    )
    runner.assertEqual(
        datastore_config.latency.put_latencies.latencies.weights,
        DS_CONFIG["latency"]["PUT"][0].values()
    )


