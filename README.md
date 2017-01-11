gchaos: Chaos Module for Google App Engine 
==========================================

Injects hooks around google app engine stubs to trigger errors. In the future
we hope to support latency adjustments, straight patching, tracing actions, etc.

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

`CONFIG = {
    'enabled': Bool,
    'errors': {
        str: ([str], float),
    },
    'latency': None
}`

#### Example

`CONFIG = {
    'enabled': True,
    'errors': {
        "DELETE": ({gchoas.utils.full_name(
            google.appengine.api.datastore_errors.BadValueError): 1}, 0.05),
        "GET": ({'google.appengine.api.datastore_errors.Timeout': 1}, 0.01),
        "PUT": ({'google.appengine.api.datastore_errors.BadRequestError': 0.75
                 'google.appengine.api.datastore_errors.InternalError': 0.25
                }, 0.02),
    },
    'latency': None
}`

The list of supported Google Datastore errors can be found here:
`google-cloud-sdk/platform/google_appengine/google/appengine/api/datastore_errors.py`

### Install

TODO: Add pip install instructions for github project
TODO: Add pip install instructions once pushed to pypi


### Usage

Once you have gchoas installed and you've modiified the config to your liking
you add these 2 lines to the end of your file that creates the wsgi app that
you setup.

Import the install function.

`from gchaos import install_chaos

Call the install method. This will use the default configuration.
`install_chaos()`

If you would like to use your on configuration pass it in here.
`install_chaos(config=YOUR_CUSTOM_CONFIG)`

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
    - Trigger the creation and read of a sample db model
      - `/example/db`
    - Trigger the creation of multiple ndb models and read of a sample ndb model
      - `/example/ndb`
    - Trigger the creation of multiple ndb models with a nested relationship
      put as a single call.
      - `/example/ndbnested`

## License

[MIT](/LICENSE)
