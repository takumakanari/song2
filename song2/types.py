#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import absolute_import


class InvalidProperty(Exception):
  pass


class _Property(object):
  typ = None

  def __init__(self, nullable=True, empty=True, default=None):
    self.nullable = nullable
    self.empty = empty
    self.default = default
    self.is_rewritable = False

  def rewritable(self):
    self.is_rewritable = True
    return self

  def validate(self, name, v):
    if v is None:
      if not self.nullable:
        raise InvalidProperty('"%s" is not nullable' % name)
      else:
        return
    if not v and not self.empty:
      raise InvalidProperty('"%s" should be non-empty value' % name)
    self._validate_type(v, self.typ, name=name)
    self.post_validate(v)

  def _validate_type(cls, v, valid_types, name=None):
    if valid_types and not isinstance(v, valid_types):
      raise InvalidProperty('"%s"=%s must be %s type, but %s' % (name, v, valid_types, type(v)))

  def post_validate(self, v):
    pass


class String(_Property):
  typ = (basestring,)


class Int(_Property):
  typ = (int,)

  def __init__(self, default=0):
    super(Int, self).__init__(nullable=False, empty=True, default=default)


class Float(Int):
  typ = (float,)

  def __init__(self, default=0.0):
    super(Float, self).__init__(default=default)


class Long(Int):
  typ = (long,)

  def __init__(self, default=0L):
    super(Long, self).__init__(default=default)


class Bool(_Property):
  typ = (bool,)

  def __init__(self, default=False):
    super(Bool, self).__init__(nullable=False, empty=True, default=default)


class Nested(_Property):

  def __init__(self, cls, nullable=True, empty=True, default=None):
    self.typ = (cls,)
    super(Nested, self).__init__(nullable=nullable, empty=empty, default=default)


class ArrayOf(_Property):
  typ = (list, tuple)

  def __init__(self, cls, nullable=True, empty=True, default=[]):
    self.valid_types = (cls,)
    super(ArrayOf, self).__init__(nullable=nullable, empty=empty, default=default)

  def post_validate(self, values):
    for v in values:
      self._validate_type(v, self.valid_types)
