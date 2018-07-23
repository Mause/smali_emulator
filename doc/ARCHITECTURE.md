# Dalvik Virtual Machine

The Dalvik Virtual Machine is register based.

It means that, in a given frame, all the registers have a given value.

This documentation may not be necessary up-to-date as we are trying to update
our architecture to answer to more demanding challenges.

# Implementation of static private fields read/write operations

What the capability is of smali_emulator right now is

- take a smali file
- execute a method in that file by passing the argument dict
- get back the result

So far, the behaviour of the emulator has been perfect in this framework. Absolutely
no errors, the software behaves very well. However, we lack many features in order 
to be absolutely able to execute arbitrary smali code:

- Cross references through the file are _not_ supported.
- Instanciation of objects is _not_ supported.

There is a real need to be able to instanciate classes « live ». Let 
us assume that the class is self-contained.

The need would be then to 

- Instanciate the class using its `<init>` method
- Execute some static methods on the object

Problem is:

  - how to dynamically create a class at runtime in python

Solution would be:
  - use the metaclass capability of python
 
Process would be:
  - parse the smali code
  - create dynamically the class object
  - 


