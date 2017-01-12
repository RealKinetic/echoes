gchaos: Chaos Module for Google App Engine 
==========================================

Injects hooks around google app engine stubs to trigger errors and latency spikes. 
In the future we hope to support straight patching, tracing actions, etc.

Currently there is a configuration done in a python module in 
`gchaos/config/datastore.py` that is the default config. You can override this
configuration in the setup method. You can change any of these configuration
entries. Currently we only support an in memory configuration but we hope to
support yaml based configurations and a web interface to change options on 
demand.

This supports both local development and deployed to a google project appengine
host.

### Configuration

#### Schema

``` python
CONFIG = {
    'datastore': {
        'enabled': Bool,
        'errors': (Bool, {
            str: ([str], float),
        }),
        'latency': (Bool, {
            str: ([str], float),
        })
    }
}
```

#### Example

``` python
CONFIG = {
    'datastore': {
        'enabled': True,
        'errors': (True, {
            "DELETE": (
                { gchaos.utils.full_name(google.appengine.api.datastore_errors.BadValueError): 1 }, 
                0.05
            ),
            "GET": ({ 'google.appengine.api.datastore_errors.Timeout': 1 }, 0.01),
            "PUT": (
                { 'google.appengine.api.datastore_errors.BadRequestError': 0.75
                'google.appengine.api.datastore_errors.InternalError': 0.25
                },
                0.02
            ),
        }),
        'latency': (True, {
            "DELETE": ( (500, 1000), 0.05),
            "GET": ( (1500,), 0.05),
            "PUT": ( 2500, 0.05)
            ),
        })
    }
}
```

You can disable the entire datastore configuration. If you set the `enabled` flag
to `False` nothing will happer. If it's set to true it will then look for errors
and latency configrations when it hits a support actions.

There are 3 datastore action types. `DELETE`, `GET`, `PUT`. You can configure different
rates which trigger the likely hood of either an error latency spike being hit.
For example above the `DELETE` error rate is set to `0.05`. The minimum is `0.00`
which means nothing will happen. Where the maximum is `1.00` which means an error
or latency spike is guranteed to happen. Otherwise it is just probabistic. Also
each action is independent of the previous action. Meaning that we don't increase
or decrease the likelyhood of an action being trigger based off subsequent actions.

##### Errors

To configure errors you create a dicionary of errors with the key being a datastore
error path. This must be a string. So you can either add the full path as a string
or if you're configuring with python you can import the error directly and use
our provided `gchaos.utils.full_name` function to get the string version.  The 
list of supported Google Datastore errors can be found here:
`google-cloud-sdk/platform/google_appengine/google/appengine/api/datastore_errors.py`

For each entry in the dictionary you then add a corresponding integer for the
error to be hit. The entries should add up to 100. This way you can say a specific
error should have a 50% likely hood of being hit by setting it's value to `50`
while you set the other two to `25` and `25` to give them a 25% chance of firing.

##### Latency

To configure latency you once again add an entry for each action. These entries
are a tuple (or list if json|yaml). The second value is the probability of the 
latency triggering. The first value of the tuple is the actual time you want
the latency spike to last for. This is tracked in millisecond (1000 milliseconds
equals 1 second). This accepts 3 types of values. Just an integer. So above
the `PUT` latency action is set to `2500` so the spike will last `2.5` seconds.
You can also provide a tuple. If the tuple only has a single value then it will
work just as if you gave us the direct integer not wrapped in the tuple. So above
the `GET` latency action has `(1500,)` set so the spike with last `1.5` seconds.
The third option is to add two entries to the tuple. This gives you a range of
latencies that we will pick a random number between. So above the `DELETE` latency
action is set to `(500, 1000)`. This means a number between `500` and `1000` will
be randomly accepted. So for example you could end up with `700` or `0.7` seconds
with this configuration. Note the second entry must be larger than the first
otherwise an error will be raised at runtime (we may move this to app initialization
time in the future). Also there can only be 1 or 2 entries in the list. Any more
or less and an error will be raised.

### Install

Pip Install

`pip install git+git://github.com/RealKinetic/gchaos.git#egg=master`

Add to requirements.txt

`-e git://github.com/RealKinetic/gchaos.git#egg=master`

TODO: Add pip install instructions once pushed to pypi


### Usage

Once you have gchaos installed and you've modiified the config to your liking
you add these 2 lines to the end of your file that creates the wsgi app that
you setup.

    # Import the install function.
    from gchaos import install_chaos

    # Call the install method. This will use the default configuration.
    install_chaos()

    # If you would like to use your on configuration pass it in here.
    install_chaos(config=YOUR_CUSTOM_CONFIG)

Then just run your app for local or deploy to a google project app engine 
project.

### Example

You can also run the example app either locally or deployed. It is setup in
the top level app.yaml.

#### Running Local

`make run`

#### Triggering examples

There are different endpoints you can hit to trigger the examples. We hope to
support a user interface in the future.

Right now when triggering the examples you'll need to monitor the logs to see
what if any exception is raised. We don't currently write to the page. However
if an execption is raised you should see a standard 500 Interal Error page.

##### Examples

Trigger the creation and read of a sample db model

`$ curl -i /example/db`
 
Trigger the creation of multiple ndb models and read of a sample ndb model

`$ curl -i /example/ndb`

Trigger the creation of multiple ndb models with a nested relationship put as a single call.

`$ curl -i /example/ndbnested`

## License

[MIT](/LICENSE)
