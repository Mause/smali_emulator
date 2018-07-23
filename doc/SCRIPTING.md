# Scripting with smali emulator

Ultimately, scripting the emulator to run methods of a `.smali` file
from a python shell is a desirable goal.

Here we attempt to write a self-explaining document, some of the features
described here may not have been implemented yet, but we are working on it :)

## Script 1

Current state of scripting API allows us to do the following:

```python

import os.path
import smali
import smali.source
import smali.emulator

static_class_path = os.path.join(
    os.path.dirname(smali.__file__), 
    os.pardir, os.pardir, 'tests', 'staticmethod', 'value_cannot_be_null.smali'
)

# create a new emulator
emulator = smali.emulator.Emulator()

# run the *only* method in that file
result = emulator.run_file(static_class_path, {'p0': 1, 'p1': 1, 'p2': -1})

# display the result
print(result)
```

## Script 2

What we would like is to do:

```python

import os.path
import smali
import smali.source
import smali.emulator

static_class_path = os.path.join(
    os.path.dirname(smali.__file__), 
    os.pardir, os.pardir, 'tests', 'staticmethod', 'value_cannot_be_null.smali'
)

# create a new emulator
emulator = smali.emulator.Emulator()

# load all the methods in that file
emulator.load_class(static_class_path)

# exec the method
emulator.exec_method('a', args={'p0': 1, 'p1': 1, 'p2': -1})

# display the result
print(result)
```

# Script 3: invoke init and subsequent methods

We want ultimately the possibility to exec methods on the fly,
especially to call the init method initializing members,
then to call method for the sget/sput/iget/iput support to be really effective.

This is possible through this example (see also `test_scripting_api.py`
for details)


```python
"""Test two successive calls: 
- first on '<clinit>' for initializing static fields
- second on 'a' for deciphering some string
"""
emulator = smali.emulator.Emulator()
emulator.load_class(get_file_path('completeclass', 'full_static_class.smali'))
res = emulator.exec_method('<clinit>', args=None)  # call the static constructor
res = emulator.exec_method(
     'a', args={'p0': p0, 'p1': p1, 'p2': p2},
     vm=emulator.vm  # need to propagate the vm because it contains
                     # the static fields initialized from call to <clinit>
)
```
