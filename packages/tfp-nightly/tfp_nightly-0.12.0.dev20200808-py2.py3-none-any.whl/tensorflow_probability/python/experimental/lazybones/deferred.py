# Copyright 2020 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
# Lint as: python3
"""Graphify anything and everything."""

from __future__ import absolute_import
from __future__ import division
# [internal] enable type annotations
from __future__ import print_function

import builtins
import functools

import tensorflow.compat.v2 as tf

from tensorflow_probability.python.experimental.lazybones import deferred_scope
from tensorflow_probability.python.experimental.lazybones import special_methods
from tensorflow_probability.python.experimental.lazybones import weak_container


__all__ = [
    'Deferred',
    'DeferredBase',
    'DeferredInput',
]


# This alias exists for docstring and code readability.
UNKNOWN = deferred_scope.UNKNOWN


# Lazily load `from IPython.lib.pretty import pretty as ipython_repr`.
ipython_repr = None


class DeferredBase(special_methods.SpecialMethods):
  """Base class for all `lazybones.backend` deferred objects."""

  __slots__ = ('_parents', '_children', '_static_iter_len', '_name',
               '__weakref__')

  def __init__(self, parents=None, static_iter_len=-1, name='<unknown>'):
    self._parents = set(() if parents is None else parents)
    self._children = weak_container.WeakSet()
    for p in self._parents:
      p._children.add(self)
    self._static_iter_len = static_iter_len
    self._name = name

  @property
  def name(self):
    return self._name

  @property
  def value(self):
    return deferred_scope.DeferredScope.current_scope[self]

  @value.setter
  def value(self, value):
    deferred_scope.DeferredScope.current_scope[self] = value
    for c in self.children:
      c.reset()

  @property
  def parents(self):
    return deferred_scope.PrettyPrintTuple(self._parents)

  @property
  def children(self):
    return deferred_scope.PrettyPrintTuple(self._children)

  def reset(self):
    # It might seem like you'd want `reset` to `del` the corresponding
    # `DeferredScope` key, i.e.,
    #   del DeferredScope.current_scope[self]
    # However this is not right. If we `reset` in the current scope then we want
    # that to be a subsequent "scope hit". I.e., we need the value to be
    # explicitly `UNKNOWN` to "block" cache hitting on "higher up" scope
    # contexts.
    self.value = UNKNOWN

  def eval(self):
    raise AttributeError('Must be defined.')

  def __action__(self, fn, *args, **kwargs):
    return Deferred(fn, *args, **kwargs)

  def __call__(self, *args, **kwargs):
    return self.__action__(self, *args, _action_name=self.name, **kwargs)

  def __dir__(self):
    s = set(object.__dir__(self))
    s.update(dir(self.eval()))
    return list(s)

  def __hash__(self):
    return object.__hash__(self)

  @functools.wraps(builtins.iter)
  def __iter__(self, *sentinel):
    if getattr(self, 'fn', None) is builtins.iter:
      if sentinel != getattr(self, 'args', (None,))[1:]:
        raise ValueError(
            'Taking `iter` of `iter` with different sentinel '
            'is not supported.')
      return self  # iter is idempotent.
    return self.__action__(
        builtins.iter, self, *sentinel, _action_name='__iter__')

  @functools.wraps(builtins.next)
  def __next__(self, *default):
    static_num_iter = (-1 if not self.parents
                       else self.parents[0]._static_iter_len)  # pylint: disable=protected-access
    if getattr(self, 'fn', None) is not builtins.iter or static_num_iter < 1:
      # In this branch we presume the user does not wish to have static
      # iteration, i.e., we defer the operation as we would any other.
      return self.__action__(
          builtins.next, self, *default, _action_name='__next__')
    next_children = tuple(c for c in self._children
                          if getattr(c, 'fn', None) is builtins.next)
    if len(next_children) < static_num_iter:
      # Here we leverage the fact that `next` accepts a second arg which is
      # the default to return if the iterator is exhausted. In fact this
      # situation can never occur because we pre-empt it above. Despite never
      # occuring we still need to pass this second arg (`self.children`) to
      # induce all the prior `next`s to be evaluated first thus forcing the
      # side-effect in the eventually concretized iterator.
      return self.__action__(
          builtins.next, self, next_children, _action_name='__next__')
    if default:
      return default
    raise StopIteration

  def __repr__(self):
    repr_no_eval = self._repr_no_eval()
    if self.value is UNKNOWN:
      return repr_no_eval
    try:
      val_str = self._to_string(repr)
    except Exception as e:  # pylint: disable=broad-except
      val_str = '"{}:{}"'.format(type(e).__name__, str(e))
    val_str = ' '.join(val_str.split())
    return '{} value={}>'.format(repr_no_eval[:-1], val_str)

  def __str__(self):
    return self._to_string(str)

  def _repr_pretty_(self, p, cycle):
    """Basically `__repr__` but as used by Ipython and Jupyter Notebook."""
    # https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html#extending
    if cycle:
      return
    global ipython_repr
    if ipython_repr is None:  # pylint: disable=used-before-assignment
      try:
        from IPython.lib.pretty import pretty as ipython_repr  # pylint: disable=g-import-not-at-top,redefined-outer-name
      except (ModuleNotFoundError, ImportError):
        ipython_repr = repr
    p.text(self._to_string(ipython_repr))

  def _to_string(self, op):
    """Returns sting version of self as implemented by `op`."""
    val = self.eval()
    # To prevent infinite recursion, don't stringify `val` when it's a
    # `DeferredBase`. The only way `val` can be `DeferredBase` is when the
    #  user does `deferred.value = Deferred*(...)`.
    # Note: when `val` is a `DeferredBase` it doesn't always mean we'd
    # infinitely recurse, however for safety reasons we don't even try.
    # Obviously we could muck with `sys.setrecursionlimit(...)` however we view
    # this as complex to get right and possibly computationally wasteful. Anyone
    # setting the (supposedly) concretized value to a `DeferredBase` either made
    # a mistake or already knows exactly what they're doing.
    if isinstance(val, DeferredBase):
      return val._repr_no_eval()  # pylint: disable=protected-access
    return op(val)

  def _repr_no_eval(self):
    """Returns `repr(self)` except never with 'value=...'."""
    # Used by: __repr__, _to_string, and deferred_scope.PrettyPrintTuple.
    return '<{} "{}">'.format(type(self).__name__, self.name)

  @staticmethod
  def _get_deferred(inputs):
    # TODO(jvdillon): use `vars` to recurse into classes/closures.
    return set(x for x in tf.nest.flatten(inputs)
               if isinstance(x, DeferredBase))


class Deferred(DeferredBase):
  """Defers execution of callable."""

  __slots__ = ('_fn', '_args', '_kwargs')

  def __new__(cls, fn, *args, **kwargs):
    static_iter_len = kwargs.pop('_static_iter_len', -1)
    name = kwargs.pop('_action_name', _try_get_name(fn, name_fallback='?'))
    parents = cls._get_deferred([fn, args, kwargs])
    if not parents:
      return fn(*args, **kwargs)
    self = super(Deferred, cls).__new__(cls)
    super(Deferred, self).__init__(
        parents, static_iter_len=static_iter_len, name=name)
    return self

  def __init__(self, fn, *args, **kwargs):  # pylint: disable=super-init-not-called
    # Note: `super` is called from `__new__` so we can recycle use of `parents`.
    kwargs.pop('_static_iter_len', None)
    kwargs.pop('_action_name', None)
    self._fn = fn
    self._args = args
    self._kwargs = kwargs

  @property
  def fn(self):
    return self._fn

  @property
  def args(self):
    return self._args

  @property
  def kwargs(self):
    return self._kwargs

  def eval(self):
    if self.value is not UNKNOWN:
      return self.value
    fn, args, kwargs = tf.nest.map_structure(
        lambda x: x.eval() if isinstance(x, DeferredBase) else x,
        [self.fn, self.args, self.kwargs])
    self.value = fn(*args, **kwargs)
    return self.value


class DeferredInput(DeferredBase):
  """Defers execution of input."""

  __slots__ = ()

  def __init__(self, value=UNKNOWN, name='input', _static_iter_len=-1):  # pylint: disable=invalid-name
    super(DeferredInput, self).__init__(
        parents=self._get_deferred(value),
        static_iter_len=_static_iter_len,
        name=name)
    if value is not UNKNOWN:
      self.value = value

  def eval(self):
    def _concretize(v):
      if v is UNKNOWN:
        raise ValueError(
            'Must assign value to `{}` object named "{}".'.format(
                type(self).__name__, self.name))
      if isinstance(v, DeferredBase):
        return v.eval()
      return v
    return tf.nest.map_structure(_concretize, self.value)


def _try_get_name(fn, name_fallback='unknown'):
  if isinstance(fn, DeferredBase):
    return fn.name
  return str(getattr(fn, '__name__', None) or
             getattr(type(fn), '__name__', name_fallback))
