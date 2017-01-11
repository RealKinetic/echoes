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

import webapp2

from google.appengine.ext import db
from google.appengine.ext import ndb

# TODO: Add some async handlers
# TODO: Add delete handlers
# TODO: Add nested delete handlers


class NdbModel(ndb.Model):

    _use_cache = False
    _use_memcache = False

    a_property = ndb.StringProperty()


class ParentModel(ndb.Model):

    _use_cache = False
    _use_memcache = False

    a_property = ndb.StringProperty()


class ChildModel(ndb.Model):

    _use_cache = False
    _use_memcache = False

    a_property = ndb.StringProperty()


class DbModel(db.Model):

    a_property = db.StringProperty()


class DBTestHandler(webapp2.RequestHandler):

    def get(self):
        db_model = DbModel(a_property="test value")
        db_model.put()

        logging.info("PUT db model: {0}".format(db_model))

        get_db_model = DbModel.get(db_model.key())

        logging.info("LOAD db model: {0}".format(get_db_model))

        assert get_db_model.key() == db_model.key()


class NDBTestHandler(webapp2.RequestHandler):

    def get(self):
        ndb_model = NdbModel(a_property="test value")
        ndb_model.put()

        logging.info("PUT ndb model: {0}".format(ndb_model))

        ndb_parent_model = ParentModel(id="parent")
        ndb_parent_model.put()

        ndb_child_model = ChildModel(id="child", parent=ndb_parent_model.key)
        ndb_child_model.put()

        get_ndb_model = ndb_model.key.get()

        logging.info("LOAD ndb model: {0}".format(get_ndb_model))

        assert get_ndb_model.key == ndb_model.key


class NDBNestedTestHandler(webapp2.RequestHandler):

    def get(self):
        ndb_parent_model = ParentModel(id="parent")
        ndb_parent_model.put()

        ndb_child_model = ChildModel(id="child", parent=ndb_parent_model.key)

        result = ndb.put_multi([ndb_parent_model, ndb_child_model])

        logging.info("PUT ndb model: {0}".format(result))

        get_ndb_model = ndb_parent_model.key.get()

        logging.info("LOAD ndb model: {0}".format(get_ndb_model))

        assert get_ndb_model.key == ndb_parent_model.key
