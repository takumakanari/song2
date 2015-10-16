#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import absolute_import

import copy

class InvalidValue(ValueError):
  pass


class InvalidType(ValueError):

  def __init__(self, name, excepted, val):
    self.name = name
    self.excepted = excepted
    self.val = val

  def __str__(self):
    return '"%s"=%s must be %s type, but %s' % (self.name, self.val,
                                                self.excepted, type(self.val))


class _Property(object):
  typ = None
  VALIDATE_CONTINUE = 1
  VALIDATE_STOP = 2

  def __init__(self, nullable=True, empty=True, default=None):
    self.nullable = nullable
    self.empty = empty
    self._default = default
    self.is_rewritable = False

  @property
  def default(self):
    return self._default

  def rewritable(self):
    self.is_rewritable = True
    return self

  def validate(self, name, v):
    if v:
      if not isinstance(v, self.typ):
        raise InvalidType(name, self.typ, v)
      return self.VALIDATE_CONTINUE
    elif v is None:
      if not self.nullable:
        raise InvalidValue('"%s" is not nullable' % name)
    elif not self.empty:
      raise InvalidValue('"%s" should be non-empty value' % name)
    return self.VALIDATE_STOP


class String(_Property):
  typ = basestring


class Int(_Property):
  typ = int

  def __init__(self, default=0):
    super(Int, self).__init__(nullable=False, empty=True, default=default)


class Float(Int):
  typ = float

  def __init__(self, default=0.0):
    super(Float, self).__init__(default=default)


class Long(Int):
  typ = long

  def __init__(self, default=0L):
    super(Long, self).__init__(default=default)


class Bool(_Property):
  typ = bool

  def __init__(self, default=False):
    super(Bool, self).__init__(nullable=False, empty=True, default=default)


class Nested(_Property):

  def __init__(self, cls, nullable=True, empty=True, default=None):
    self.typ = cls
    super(Nested, self).__init__(nullable=nullable,
                                 empty=empty, default=default)


class ArrayOf(_Property):
  typ = (list, tuple)

  def __init__(self, cls, nullable=True, empty=True, default=[]):
    self.element_type = cls
    super(ArrayOf, self).__init__(nullable=nullable, empty=empty,
                                  default=default)

  @property
  def default(self):
    return copy.deepcopy(self._default)

  def validate(self, name, values):
    if super(ArrayOf, self).validate(name, values) == self.VALIDATE_CONTINUE:
      for v in values:
        if not isinstance(v, self.element_type):
          raise InvalidType(name, self.element_type, v)
