#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import absolute_import

from unittest import TestCase
from nose.tools import ok_
from nose.tools import eq_
from nose.tools import raises
from nose.tools import with_setup

from song2 import Schema, NotRewritable, UnknownProperty
from song2.types import *



class TestSchema(TestCase):

  def test_constructor(self):
    class S(Schema):
      name = String()
      age = Int()
    s = S(name='test', age=15)
    eq_(s['name'], 'test')
    eq_(s['age'], 15)

  def test_make(self):
    S = Schema.make(v1=String(), v2=Int())
    ok_(isinstance(S.v1, String))
    ok_(isinstance(S.v2, Int))
    ok_(isinstance(S(), Schema))

  def test_make_flags(self):
    S = Schema.make(allow_optional=False, merge_optional=True, immutable=False, v=String())
    eq_(S.allow_optional, False)
    eq_(S.merge_optional, True)
    eq_(S.immutable, False)

  @raises(ValueError)
  def test_make_with_invalid_property(self):
    Schema.make(v1=String(), v2='INVALID')

  @raises(NotRewritable)
  def test_not_rewritable_direct(self):
    s = Schema.make(v=String())(v='test')
    s['v'] = 'new value'

  @raises(NotRewritable)
  def test_not_rewritable_by_update(self):
    s = Schema.make(v=String())(v='test')
    s.update(v='new value')

  @raises(NotRewritable)
  def test_not_rewritable_by_merge(self):
    s = Schema.make(v=String())(v='test')
    s.update({'v' : 'new value'})

  def test_rewritable(self):
    s = Schema.make(v=String().rewritable())(v='test')
    eq_(s['v'], 'test')

    s['v'] = 'new value'
    eq_(s['v'], 'new value')

    s.update(v='new value2')
    eq_(s['v'], 'new value2')

    s.update({'v' : 'new value3'})
    eq_(s['v'], 'new value3')

  def test_allow_optional(self):
    class S(Schema):
      name = String()
      age = Int()
    s = S(name='test', age=15, optional='this is optional')
    eq_(s.get('optional'), None) # optional field will not be merged

  @raises(UnknownProperty)
  def test_disallow_optional(self):
    class S_(Schema):
      allow_optional = False
      name = String()
    s = S_(name='test', optional='this is optional')

  def test_merge_optional(self):
    class S_(Schema):
      merge_optional = True
      name = String()
    s = S_(name='test', optional='this is optional')
    eq_(s['optional'], 'this is optional')

