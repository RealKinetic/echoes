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


# So much stolen from Robert Kluin and Furious here :)
# https://github.com/WebFilings/furious

from collections import namedtuple


def full_name(obj):
    """Returns the full python name with the path as a string.

    Args:
        obj (string): Class

    Returns:
        str
    """
    return "{0}.{1}".format(obj.__module__, obj.__name__)


class BadObjectPathError(Exception):
    """Invalid object path."""


FuncInfo = namedtuple('FuncInfo', ['name', 'parent', 'func'])


def get_func_info_for_path(path):
    """Convert an object path reference to a reference."""

    path = str(path)

    if '.' not in path:
        built_ins = globals()["__builtins__"]
        try:
            return FuncInfo(path, built_ins, built_ins[path])
        except KeyError:
            try:
                return FuncInfo(path, built_ins, getattr(built_ins, path))
            except AttributeError:
                pass

        try:
            globes = globals()
            return FuncInfo(path, globes, globes[path])
        except KeyError:
            pass

        raise BadObjectPathError(
            'Unable to find function "%s".' % (path,))

    module_path, function_name = path.rsplit('.', 1)

    try:
        module = __import__(name=module_path,
                            fromlist=[function_name])
    except ImportError:
        module_path, class_name = module_path.rsplit('.', 1)

        module = __import__(name=module_path, fromlist=[class_name])
        module = getattr(module, class_name)

    try:
        return FuncInfo(function_name, module, getattr(module, function_name))
    except AttributeError:
        raise BadObjectPathError(
            'Unable to find function "%s".' % (path,))
