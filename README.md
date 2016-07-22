# song2
Typesafe/Immutable schema for dict object

The main features are:

- Typesafe schema class
- Generate immutable dict object

Useful for:

- Defining response schema for JSON API
- Mapping row dict from DB like ORM mappers
- Defining/Binding properties from config file in YAML

etc ...

### Usage

#### Schema class
It's easy to define schema class.

1. extend *song2.Schema*
2. define fields with types

```python
class Person(Schema):
  name = String()
  age = Int()
  comments = StringArray()
  hobbies = ArrayOf(Hobby)
  address = Nested(Address)
```

Also *Schema.make* is simple way to define schema class:

```python
Person = Schema.make(name=String(), age=String())
```

Then you get {dict} like object like as follows:

```python
p = Person(
  name='George',
  age=25,
  address=Address(addr='1-2-3', country='Japan'),
  hobbies=[Hobby(name='Music', years=20), Hobby(name='Cycling', years=3)],
  comments=('hello', 'goodbye')
)
p['name'] # -> 'George'
p['address'] # -> {'addr':'1-2-3', 'country':'Japan'}
p['comments'] # -> ['hello', 'goodbye']
```

#### Type classes

Property types which you can define are as below:

```python
from song2.types import *

# primitive types
String()                # -> str/unicode
StringValue()           # -> str/unicode, None/empty is not allowed
Int()/Float()/Long()    # -> int/float/long
Bool()                  # -> bool

# object
Nested(OtherSchema)     # -> Schema class (will be dict)

# arrays
ArrayOf(str)            # -> list or tuple of str
ListOf(str)             # -> list of str
TupleOf(str)            # -> tuple of str
ArrayOf(OtherSchema)    # -> list or tuple of Schema class, will be array of dict

# alias of array types
StringArray()
IntArray()
FloatArray()
LongArray()
BoolArray()
```

##### Define default value

You can customize default value of each fields.

Default value will be used if field is not set.

```python
class Person(Schema):
  name = String(default='NoName')

Person(name='John')['name'] # -> 'John'
Person()['name'] # -> 'NoName'
```

##### Nullable and allow empty

Also you can control allow null/empty value by options of Type class:


```python
class Person(Schema):
  name = String(nullable=False, empty=False)

Person(name=None) # -> ERROR!
Person() # -> ERROR!
Person(name='') # -> ERROR!
```

\* Type for number (Int/Long/Float) always allows empty(=0) and disallows null.


#### Not rewritable and rewritable

By default, a property of generated dict is **no-rewritable**.


So the follwing code raises error:

```python
p = Person(name='George')
p['name'] = 'Poul'  # Exception!
```

If you want to update it, call *rewritable()* in each fields:

```python
class Rewritable(Schema):
  rewritable_field = String().rewritable()

p = Rewritable(rewritable_field='one')

p['rewritable_field'] # -> 'one'

p['rewritable_field'] = 'two'

p['rewritable_field'] # -> 'two'
```

#### Handle optional fields

An optional fields are allowd by default.

```python
class Person(Schema):
  name = String()

p = Person(
  name='George',
  optional='this is optional'  # this field is not defined in Schema
)
p['optional'] # -> 'this is optional'
```

You can limit an optional fields by *allow_optional* and *merge_optional*.

* allow_optional: Allow or disallow optional fields, True is used by default.
* merge_optional: If True, an optional fields will be merged. If False, an optional fields will be skipped, True is used by default.

```python
class Person2(Schema):
  allow_optional = False # Disallow optional fields
  name = String()

p2 = Person2(name='George', optional='this is optional') # -> ERROR

class Person3(Schema):
  merge_optional = False # Disallow merging optional fields

p3 = Person3(name='George', optional='this is optional')
p3.keys() -> ['name']
```


### Tests & benchmarks

First, you need to install some modules to run it:

```
$ pip install -r test-and-bench-requirements.txt
```

#### Run tests

```
$ cd /path/to/project
$ nosetests nosetests tests/
```

#### Run benchmarks

```
$ cd /path/to/project
$ python bench/bench.py
```

