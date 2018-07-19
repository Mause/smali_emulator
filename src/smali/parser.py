"""
A bunch of helper function to help parsing a smali
source code listing.
"""
import re

# first token of a line (white space separated tokens)

FIRST_TOKEN = re.compile(r'([\w\-\/]+)') 
FIELD_PATTERN = re.compile(r'^\.field.*\s+(\w+):(.*)')
CLASS_PATTERN = re.compile(r'(L?)([a-zA-Z]+[\w\/]+);?')
METHOD_PATTERN = re.compile(r'^\.method.*\s+(.*)\((.*)\)(.*)$')
COMPOSITE_TYPE = re.compile(r'^(L[\w/]+;)')
ARRAY_TYPE = re.compile(r'^\[')


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
    """Get the field and type of attributes from a given line.

    >>> # 'l' is the identifier and type is '[B' (array of bytes)
    >>> get_field_name_and_type(".field public static l:[B")
    ('l', '[B')
    >>> get_field_name_and_type(".field private static r:B")
    ('r', 'B')
    """
    match_object = FIELD_PATTERN.match(source_line)
    assert match_object is not None
    return match_object.group(1, 2)

def get_composite_type(current_string):
    """Return the type of the first element in the string.
    
    >>> get_composite_type('I')
    ('I', '')
    >>> get_composite_type('Ljava/lang/Object;')
    ('Ljava/lang/Object;', '')
    >>> get_composite_type('Ljava/lang/Object;[IB')
    ('Ljava/lang/Object;', '[IB')
    """
    is_match = COMPOSITE_TYPE.match(current_string)
    return (
        (is_match.group(1), current_string.lstrip(is_match.group(1))) if is_match 
        else (current_string[0], current_string[1:])
    )

def parse_argument_list(arglist):
    """Parse a smali argument list as given in smali method 
    signature files.

    >>> parse_argument_list('IILjava/lang/Object;')
    ('I', 'I', 'Ljava/lang/Object;')
    >>> parse_argument_list('CLjava/lang/String;[C')
    ('C', 'Ljava/lang/String;', '[C')
    >>> parse_argument_list('[I[I[C')
    ('[I', '[I', '[C')
    >>> parse_argument_list('SS')
    ('S', 'S')
    """
    argument_list = ()
    current_string = arglist
    current_type = ''

    while current_string:
        if ARRAY_TYPE.match(current_string):
            current_type = current_string[0]
            current_string = current_string[1:]
            scalar_type, current_string = get_composite_type(current_string)
            current_type += scalar_type

        else:
            current_type, current_string = get_composite_type(current_string)

        argument_list = argument_list + (current_type,)
        current_type = ''

    return argument_list


def get_method_name_and_signature(source_line):
    """Get the method name and signature from a given line.

    >>> # '$$a' is the method name
    >>> # () is the list of argument types
    >>> # 'V' is the return type (void)
    >>> get_method_name_and_signature(".method static $$a()V")
    ('$$a', (), 'V')
    >>> get_method_name_and_signature(".method static constructor <clinit>()V")
    ('<clinit>', (), 'V')
    >>> get_method_name_and_signature(".method public static b(Ljava/lang/Object;)I")
    ('b', ('Ljava/lang/Object;',), 'I')
    >>> get_method_name_and_signature(".method public static c(CII)Ljava/lang/Object;")
    ('c', ('C', 'I', 'I'), 'Ljava/lang/Object;')
    """
    method_name, argument_list, return_type = METHOD_PATTERN.match(source_line).group(1, 2, 3)
    return method_name, parse_argument_list(argument_list), return_type


def extract_attribute_names(smali_source_code):
    return [get_field_name_and_type(the_line) 
            for the_line in smali_source_code.lines
            if the_line.startswith('.field')]


def extract_methods(smali_source_code):
    return [get_method_name_and_signature(the_line)
            for the_line in smali_source_code.lines
            if the_line.startswith('.method')]
