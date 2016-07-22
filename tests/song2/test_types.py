#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import absolute_import

from unittest import TestCase
from nose.tools import ok_
from nose.tools import eq_
from nose.tools import raises
from nose.tools import with_setup

from song2 import Schema, NotRewritable
from song2.types import *


class Test_Property(TestCase):
  
  def test_nullable(self):
    s = String(nullable=True)
    s.validate('test', None)

  @raises(InvalidValue)
  def test_not_nullable(self):
    s = String(nullable=False)
    s.validate('test', None)

  def test_empty(self):
    s = String(empty=True)
    s.validate('test', '')

  @raises(InvalidValue)
  def test_not_empty(self):
    s = String(empty=False)
    s.validate('test', '')

  def test_default(self):
    s = String(default='default')
    eq_(s.default, 'default')
  
  def test_set_rewritable(self):
    s = String().rewritable()
    eq_(s.is_rewritable, True)
 

class TestStringType(TestCase):

  def test_valid(self):
    s = Schema.make(v=String())(v='test')
    eq_(s['v'], 'test')
  
  def test_default(self):
    s = Schema.make(v=String())()
    eq_(s['v'], None)

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=String())(v=1234)


class TestStringValueType(TestCase):

  def test_valid(self):
    s = Schema.make(v=StringValue())(v='test')
    eq_(s['v'], 'test')
  
  @raises(InvalidValue)
  def test_not_nullable_by_default(self):
    Schema.make(v=StringValue())()

  @raises(InvalidValue)
  def test_not_empty_by_default(self):
    Schema.make(v=StringValue())(v='')

  def test_default(self):
    s = Schema.make(v=StringValue(default='ok'))()
    eq_(s['v'], 'ok')

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=StringValue())(v=1234)


class TestIntType(TestCase):

  def test_valid(self):
    s = Schema.make(v=Int())(v=123)
    eq_(s['v'], 123)

  def test_default(self):
    s = Schema.make(v=Int())()
    eq_(s['v'], 0)

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=Int())(v='test')
  
  @raises(InvalidValue)
  def test_not_nullable(self):
    Schema.make(v=Int())(v=None)


class TestFloatType(TestCase):

  def test_valid(self):
    s = Schema.make(v=Float())(v=123.0)
    eq_(s['v'], 123.0)

  def test_default(self):
    s = Schema.make(v=Float())()
    eq_(s['v'], 0.0)

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=Float())(v='test')
  
  @raises(InvalidValue)
  def test_not_nullable(self):
    Schema.make(v=Float())(v=None)


class TestLongType(TestCase):

  def test_valid(self):
    s = Schema.make(v=Long())(v=12345L)
    eq_(s['v'], 12345L)

  def test_default(self):
    s = Schema.make(v=Long())()
    eq_(s['v'], 0L)

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=Long())(v='test')
  
  @raises(InvalidValue)
  def test_not_nullable(self):
    Schema.make(v=Long())(v=None)


class TestBoolType(TestCase):

  def test_valid(self):
    s = Schema.make(v=Bool())(v=True)
    eq_(s['v'], True)

  def test_default(self):
    s = Schema.make(v=Bool())()
    eq_(s['v'], False)

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=Bool())(v='test')
  
  @raises(InvalidValue)
  def test_not_nullable(self):
    Schema.make(v=Bool())(v=None)


class TestNestedType(TestCase):

  def test_valid(self):
    s = Schema.make(v=Nested(str))(v='test')
    eq_(s['v'], 'test')

  def test_default_as_not_none(self):
    s = Schema.make(v=Nested(str, default='OK'))()
    eq_(s['v'], 'OK')

  def test_default(self):
    s = Schema.make(v=Nested(str))()
    eq_(s['v'], None)

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=Nested(str))(v=1234)


class TestArrayOfType(TestCase):

  def test_valid_list(self):
    s = Schema.make(v=ArrayOf(str))(v=['test1', 'test2'])
    eq_(s['v'], ['test1', 'test2'])

  def test_valid_tuple(self):
    s = Schema.make(v=ArrayOf(str))(v=('test1', 'test2'))
    eq_(s['v'], ('test1', 'test2'))

  def test_default(self):
    s = Schema.make(v=ArrayOf(str))()
    eq_(s['v'], [])

  def test_default_as_nonw(self):
    s = Schema.make(v=ArrayOf(str, default=None))()
    eq_(s['v'], None)

  @raises(InvalidType)
  def test_invalid(self):
    Schema.make(v=ArrayOf(str))(v=1234)

  @raises(InvalidType)
  def test_invalid_element(self):
    Schema.make(v=ArrayOf(str))(v=['test', 1])


class ListTupleOfType(TestCase):

  def test_valid_tuple(self):
    s = Schema.make(v=ListOf(str))(v=['test1', 'test2'])
    eq_(s['v'], ['test1', 'test2'])

  def test_default(self):
    s = Schema.make(v=ListOf(str))()
    eq_(s['v'], [])


class TestTupleOfType(TestCase):

  def test_valid_tuple(self):
    s = Schema.make(v=TupleOf(str))(v=('test1', 'test2'))
    eq_(s['v'], ('test1', 'test2'))

  def test_default(self):
    s = Schema.make(v=TupleOf(str))()
    eq_(s['v'], ())


class TestStringArrayType(TestCase):

  def test_valid_list(self):
    s = Schema.make(v=StringArray())(v=['test1', 'test2'])
    eq_(s['v'], ['test1', 'test2'])

  def test_valid_tuple(self):
    s = Schema.make(v=StringArray())(v=('test1', 'test2'))
    eq_(s['v'], ('test1', 'test2'))

  @raises(InvalidType)
  def test_invalid_element(self):
    Schema.make(v=StringArray())(v=['test', 1])


class TestIntArrayType(TestCase):

  def test_valid_list(self):
    s = Schema.make(v=IntArray())(v=[1, 2])
    eq_(s['v'], [1, 2])

  def test_valid_tuple(self):
    s = Schema.make(v=IntArray())(v=(1, 2))
    eq_(s['v'], (1, 2))

  @raises(InvalidType)
  def test_invalid_element(self):
    Schema.make(v=IntArray())(v=['test', 1])


