#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from benchmarker import Benchmarker
from song2 import Schema
from song2.types import *


Comment = Schema.make(name=String(), message=String())
Address = Schema.make(country=String(), city=String())


class Person(Schema):
  name = String()
  age = Int()
  hobbies = ArrayOf(str)
  comments = ArrayOf(Comment)
  address = Nested(Address)


class Person2(Schema):
  merge_optional = True

  name = String()
  age = Int()
  hobbies = ArrayOf(str)
  comments = ArrayOf(Comment)
  address = Nested(Address)


loop = 50000

with Benchmarker(loop, width=35) as bench:

  @bench('raw-dict')
  def _(bm):
    for i in bm:
      dict(
        name = 'George',
        age = 15,
        hobbies = ['music', 'soccer'],
        comments = [
          dict(name='John', message='Hello'),
          dict(name='Paul', message='Goodbye')
        ],
        address = dict(
          country = 'Japan',
          city = 'Tokyo'
        )
      )

  @bench('song2')
  def _(bm):
    for i in bm:
      Person(
        name = 'George',
        age = 15,
        hobbies = ['music', 'soccer'],
        comments = [
          Comment(name='John', message='Hello'),
          Comment(name='Paul', message='Goodbye')
        ],
        address = Address(
          country = 'Japan',
          city = 'Tokyo'
        )
      )

  @bench('song2 (merge optional)')
  def _(bm):
    for i in bm:
      Person2(
        name = 'George',
        age = 15,
        hobbies = ['music', 'soccer'],
        comments = [
          Comment(name='John', message='Hello'),
          Comment(name='Paul', message='Goodbye')
        ],
        address = Address(
          country = 'Japan',
          city = 'Tokyo'
        ),
        opt1 = 'opt1',
        opt2 = 'opt2'
      )
