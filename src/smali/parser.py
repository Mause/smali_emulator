"""
A bunch of helper function to help parsing a smali
source code listing.
"""
import re

# first token of a line (white space separated tokens)

FIRST_TOKEN = re.compile(r'([\w\-\/]+)') 
FIELD_PATTERN = re.compile(r'^\.field.*\s+(\w+):(.*)')
CLASS_PATTERN = re.compile(r'(L?)([a-zA-Z]+[\w\/]+);?')


class IncorrectPattern(Exception):
    pass


def extract_class_name(class_descriptor_string):
    """Extract a class name from a method invocation line.

    :param vm: Instance of the VM.
    :param name: The name of the class to be demangled.
    :return: The demangled class name.

    >>> extract_class_name('Ljava/lang/String;->charAt(I)C')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    IncorrectPattern: 'Ljava/lang/String;->charAt(I)C' Does not correspond to a class.
    >>> extract_class_name('Ljava/lang/reflect/Method;')
    'java.lang.reflect.Method'
    """
    match = CLASS_PATTERN.match(class_descriptor_string)
    if not (match and match.group(0) == class_descriptor_string):
        raise IncorrectPattern(
            "'{}' Does not correspond to a class.".format(class_descriptor_string)
        )

    return match.group(2).replace('/', '.').replace(';', '')


def get_op_code(input_symbol_table_line):
    """Get Op Code from Op Code List.

    >>> get_op_code("if-ne vx, vy, target")
    'if-ne'
    >>> get_op_code("nop")
    'nop'
    >>> get_op_code("cmpl-double vx, vy, vz")
    'cmpl-double'
    """
    return FIRST_TOKEN.search(input_symbol_table_line).group(1)

def get_field_name_and_type(source_line):
    """Get the field and type of attributes from a given line

    >>> # 'l' is the identifier and type is '[B' (array of bytes)
    >>> get_field_name_and_type(".field public static l:[B")
    ('l', '[B')
    >>> get_field_name_and_type(".field private static r:B")
    ('r', 'B')
    """
    match_object = FIELD_PATTERN.match(source_line)
    assert match_object is not None
    return match_object.group(1, 2)


def extract_attribute_names(smali_source_code):
    return [get_field_name_and_type(the_line) 
            for the_line in smali_source_code.lines
            if the_line.startswith('.fiel')]
