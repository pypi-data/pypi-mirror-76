[![Test Status](https://github.com/squirrel-preslash/snaked/workflows/Test%20Snaked/badge.svg)](https://github.com/squirrel-preslash/snaked/actions)

Slim. Beautiful. Snaked.

# Snaked - Snakifying Your Code For PEP8

`snaked-py` is a universal wrapper for Python objects of all kinds.
It allows you to access `camelCase` and `PascalCase` attributes of wrapped objects using
the familiar, and officially approved by the Python Software Foundation, `snake_case` syntax.

## Installation

You can install the latest stable release of `snaked-py` using pip:

`$ pip install snaked-py`

You can also clone the GitHub repository and install the package manually by running:

`$ python3 setup.py install`

## Features

- auto-enables snake_case access for camelCase objects
- autp-enables snake_case access for PascalCase objects
- wraps around any kind of object/3rd-party module/etc.
- includes runtime optimizations like caching
- PEP8-compliant and lightweight with only one dependency

## Why should I use Snaked?

PEP8 (Python Enhancement Proposal 8, the official definition of Python coding standards)
proposes the use of snake_case syntax throughout your code. However, it also states that
consistency has more preference compared to PEP8 compliance.

If a 3rd-party module uses camelCase while you stick to to the official snake_case, you will
have inconsistent code syntax which violates the PEP8. Using camelCase for all your code however,
doesn't fully comply with PEP8 either.

`Snaked` solves this problem by providing convenient wrapper utilities for accessing your
camelCase objects using the preferred snake_case syntax.


## Example Usage

Let's use the following class in this example:

```
class Camel(object):
    def createMe(self, name):
        self.name = name
    def sayHello(self):
        print("Hey, I'm", self.name)
```

Usual access:

```
>>> animal = Camel()
>>> animal.createMe("Mr. C. Java")
>>> animal.sayHello()
Hey, I'm Mr. C. Java
```

Snaked Access:

```
>>> from snaked import Snaked
>>> animal = Snaked(Camel())
>>> animal.create_me("Mr. C. Python")
>>> animal.say_hello()
Hey, I'm Mr. C. Python
```

## Edge Cases

Snaked uses resolution-caching by default to improve performance.
In some rare situations, you might remove camelCase/pascalCase-attributes
of your wrapped objects and re-introduce them in a different case.

Example:

```
>>> original = Camel()
>>> animal = Snaked(original)
>>> animal.create_me("Mr. Ed")
>>> animal.say_hello()
>>> original.SayHello = original.sayHello
>>> del original.sayHello
>>> animal.say_hello()
AttributeError: 'Cameleon' object has no attribute 'sayHello'
```

You will then have to clear the resolution cache to let Snaked search again for the
corresponding new camelCase/PascalCase/snake_case version:

```
>>> original.SayHello = original.sayHello
>>> del original.sayHello
>>> from snaked import clear_cache
>>> clear_cache(animal)
>>> animal.say_hello()
Hey, I'm Mr. Ed
```

---------------------------------

You can also circumvent this situation by preventing Snaked from caching resolved attributes.
Note however, that this will decrease your program's performance drastically.

```
animal = Snaked(original, use_cache=False)
```

## License

This project is licensed under the MIT license by Squirrel-Preslash.
It is free to use for any commercial or non-commercial purpose.

If you do so, you are required to include the full license text in a special section of your
compiled program (i.e. in a credits or startup screen) or a copy of the license in the distributed
source code.
