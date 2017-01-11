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


from google.appengine.api import datastore_errors

from gchaos.utils import full_name

# GOOGLE FILE
# google-cloud-sdk/platform/google_appengine/google/appengine/api/datastore_errors.py

# Set error names
DELETE = 'DELETE'
GET = 'GET'
PUT = 'PUT'

# Set error rates
DELETE_ERROR_RATE = 0.05
GET_ERROR_RATE = 0.01
PUT_ERROR_RATE = 0.02

# Configure error types
DELETE_ERRORS = {
    full_name(datastore_errors.BadValueError): 5,
    full_name(datastore_errors.BadRequestError): 5,
    full_name(datastore_errors.InternalError): 20,
    full_name(datastore_errors.Timeout): 70,
}

GET_ERRORS = {
    full_name(datastore_errors.BadValueError): 5,
    full_name(datastore_errors.BadRequestError): 5,
    full_name(datastore_errors.EntityNotFoundError): 5,  # ERROR IS DEPRECATED
    full_name(datastore_errors.InternalError): 10,
    full_name(datastore_errors.Timeout): 75,
}

PUT_ERRORS = {
    full_name(datastore_errors.BadValueError): 5,
    full_name(datastore_errors.BadRequestError): 5,
    full_name(datastore_errors.InternalError): 10,
    full_name(datastore_errors.Timeout): 80,
}

DEFAULT_LATENCY = (500, 10000)
DELETE_LATENCY_RATE = 0.05
GET_LATENCY_RATE = 0.01
PUT_LATENCY_RATE = 0.02

DELETE_LATENCY = {
    full_name(datastore_errors.BadValueError): DEFAULT_LATENCY,
    full_name(datastore_errors.BadRequestError): DEFAULT_LATENCY,
    full_name(datastore_errors.InternalError): DEFAULT_LATENCY,
    full_name(datastore_errors.Timeout): DEFAULT_LATENCY,
}

GET_LATENCY = {
    full_name(datastore_errors.BadValueError): DEFAULT_LATENCY,
    full_name(datastore_errors.BadRequestError): DEFAULT_LATENCY,
    full_name(datastore_errors.EntityNotFoundError): DEFAULT_LATENCY,  # ERROR IS DEPRECATED
    full_name(datastore_errors.InternalError): DEFAULT_LATENCY,
    full_name(datastore_errors.Timeout): DEFAULT_LATENCY,
}

PUT_LATENCY = {
    full_name(datastore_errors.BadValueError): DEFAULT_LATENCY,
    full_name(datastore_errors.BadRequestError): DEFAULT_LATENCY,
    full_name(datastore_errors.InternalError): DEFAULT_LATENCY,
    full_name(datastore_errors.Timeout): DEFAULT_LATENCY,
}

# Wrap it all up into the CONFIG variable
CONFIG = {
    'enabled': True,
    'errors': {
        DELETE: (DELETE_ERRORS, DELETE_ERROR_RATE),
        GET: (GET_ERRORS, GET_ERROR_RATE),
        PUT: (PUT_ERRORS, PUT_ERROR_RATE),
    },
    'latency': {
        DELETE: (DELETE_LATENCY, DELETE_LATENCY_RATE),
        GET: (GET_LATENCY, GET_LATENCY_RATE),
        PUT: (PUT_LATENCY, PUT_LATENCY_RATE),
    }
}

# Place CONFIG in the list of publically available variables
__all__ = [CONFIG]
