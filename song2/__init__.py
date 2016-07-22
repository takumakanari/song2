#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import absolute_import

__song2__ = 'song2'
__version__ = '0.1.3'
__author__ = 'Takumakanari'
__license__ = 'MIT'
__description__ = 'Typesafe/Immutable schema for dict object'


from song2.types import _Property


class UnknownProperty(Exception):

  def __init__(self, schema, name):
    self.schema = schema
    self.name = name

  def __str__(self):
    return '<%s> unknown property "%s"' % (self.name, self.schema)


class NotRewritable(Exception):

  def __init__(self, name):
    self.name = name

  def __str__(self):
    return '%s is not rewritable field after generate object' % self.name


class Schema(dict):
  __typefields__ = None
  allow_optional = True
  merge_optional = False
  immutable = True

  def __init__(self, **kwargs):
    self._disable_update_property = False
    fields = self._typefields()
    instance = super(Schema, self)
    for k, value_type in fields:
      try:
        v = kwargs[k]
      except KeyError:
        v = value_type.default
      value_type.validate(k, v)
      instance.__setitem__(k, v)
    if self.merge_optional or not self.allow_optional:
      self._handle_optional_values(fields, kwargs)
    self._disable_update_property = self.immutable

  @property
  def json(self):
    return self

  @classmethod
  def _typefields(cls):
    if cls.__typefields__ is None:
      pf = []
      for name in dir(cls):
        value = getattr(cls, name)
        if isinstance(value, _Property):
          pf.append((name, value))
      cls.__typefields__ = pf
    return cls.__typefields__

  @classmethod
  def make(cls, allow_optional=True, merge_optional=False,
           immutable=True, **kwargs):
    """
     Provides dynamic making {Schema} class like as follows:
       ```
       Comment = Schema.make(name=types.String(), message=types.String())
       ```
    """
    class _Dynamic(Schema):
      pass
    for prop, typ in kwargs.items():
      if not isinstance(typ, _Property):
        raise ValueError('"%s" should be instance of %s' % (prop, _Property))
      setattr(_Dynamic, prop, typ)
    setattr(_Dynamic, 'allow_optional', allow_optional)
    setattr(_Dynamic, 'merge_optional', merge_optional)
    setattr(_Dynamic, 'immutable', immutable)
    return _Dynamic

  def __setitem__(self, key, value):
    self._assert_is_writable(key, value)
    super(Schema, self).__setitem__(key, value)

  def update(self, *args, **kwargs):
    for src in args:
      for k, v in src.items():
        self[k] = v
    for k, v in kwargs.items():
      self[k] = v

  def _handle_optional_values(self, fields, inputs):
    field_keys = map(lambda x: x[0], fields)
    instance = super(Schema, self)
    for ik in inputs.keys():
      if ik not in field_keys:
        if not self.allow_optional:
          raise UnknownProperty(self.__class__.__name__, ik)
        instance.__setitem__(ik, inputs[ik])

  def _assert_is_writable(self, name, value):
    value_type = getattr(self, name)
    if self._disable_update_property and not value_type.is_rewritable:
      raise NotRewritable(name)
    value_type.validate(name, value)
