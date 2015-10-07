#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from song2 import Schema
from song2.types import *


Address = Schema.make(addr=String(), country=String())
Hobby = Schema.make(name=String(), years=Int())
Frend = Schema.make(name=String(), age=Int())


class Person(Schema):
  merge_optional = True

  name = String()
  age = Int()
  boy = Bool()
  address = Nested(Address)
  hobbies = ArrayOf(Hobby)
  comments = ArrayOf(str)
  try_default = String(default='this is default')
  floatproperty = Float()
  longproperty = Long()
  frends = ArrayOf(Frend)


if __name__ == '__main__':
  print Person(
    name='George',
    age=25,
    address=Address(addr='1-2-3', country='Japan'),
    boy=True,
    hobbies=[Hobby(name='Music', years=20), Hobby(name='Cycling', years=3)],
    comments=('hello', 'goodbye'),
    unknown='OK',
    floatproperty = 1.4,
    longproperty = 5L,
    frends = [Frend(name='Michel', age=5)]
  ).json