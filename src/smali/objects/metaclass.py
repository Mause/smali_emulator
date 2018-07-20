"""Metaclass used to dynamically create classes for smali files."""

import os.path

from ..source import (
    get_source_from_file,     # get source object from a file path
)

from ..parser import (
    extract_methods,          # extract method from a source object
    extract_attribute_names,  # extract attributes from a source object
)

class MetaJavaClass(type):
    def __new__(metacls, classname, parent_classes, attr_and_methods):
        return type.__new__(metacls, classname, parent_classes, attr_and_methods)

    def __init__(self, classname, parent_classes, attr_and_methods):
        super(MetaJavaClass, self).__init__(classname, parent_classes, attr_and_methods)


def setUpAttributes(attributeFields, methodFields):
    """Set Up the metaclass attributes, namely:
        - the fields (usually static or private or public)
        - the methods (trickier to implement method calling, not done at the moment)

    The return result is a dict that can be provided to the __new__ metaclass
    method.
    """
    attributeResultingDict = {}
    for fieldName, fieldType in attributeFields:
        attributeResultingDict[fieldName] = None

    for (methodName, argumentList, returnType), smaliSource in methodFields.items():
        def function_call(self, *args, **kwargs):
            raise NotImplementedError()

        attributeResultingDict[methodName] = function_call

    return attributeResultingDict


def getClassFromSmali(filename):
    """Return a class mimicking the behaviour of the underlying Smali Code.
    
    - The first step is to parse the smali file and fetch elementary informations 
      from it.
    - The second step is to build the class according to the parsed content.
    - Third step is to allow class instanciation execution
    - Fourth step is to allow arbitrary code execution from this class.
    """
    sourceCode = get_source_from_file(filename)
    className = os.path.basename(filename).title()

    return MetaJavaClass(
        className, (object, ),
        setUpAttributes(
            extract_attribute_names(sourceCode),
            extract_methods(sourceCode)
        )
    )