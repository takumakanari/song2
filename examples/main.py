#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from song2 import Schema
from song2.types import *


Address = Schema.make(addr=String(), country=String())
Hobby = Schema.make(name=String(), years=Int())


class Prop(Schema):
  text = StringValue()


class Person(Schema):
  name = String()
  age = Int()
  comments = StringArray()
  hobbies = ArrayOf(Hobby)
  address = Nested(Address)
  try_default = StringValue(default='this is default')
  floatproperty = Float()
  longproperty = Long()
  dynamic_dict = StringDict(Prop)


class Rewritable(Schema):
  rewritable_field = String().rewritable()


class DefaultValue(Schema):
  message = String(default='please enter a message')


def dump(s):
  try:
    import json
    print json.dumps(s.json)
  except ImportError:
    print p.json


if __name__ == '__main__':
  p = Person(
    name='George',
    age=25,
    address=Address(addr='1-2-3', country='Japan'),
    hobbies=[Hobby(name='Music', years=20), Hobby(name='Cycling', years=3)],
    comments=('hello', 'goodbye'),
    dynamic_dict = {
      'field1' : Prop(text='hello!'),
      'field2' : Prop(text='goodbye!')
    }
  ).json
  dump(p)

  p = Rewritable(rewritable_field='one')
  p['rewritable_field'] = 'two'
  dump(p)

  p1 = DefaultValue()
  p2 = DefaultValue(message='here is message')
  print p1
  print p2
