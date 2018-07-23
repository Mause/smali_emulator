import os.path

import pytest

import smali
import smali.source
import smali.emulator

def get_file_path(datadir, filename):
    return os.path.join(
        os.path.dirname(smali.__file__),
        os.pardir, os.pardir, 'tests',
        datadir, filename
    )

def test_script_number_one():
    """Test that scripting mode behaves correctly."""

    # create a new emulator
    emulator = smali.emulator.Emulator()

    # load all the methods in that file
    emulator.load_class(get_file_path('staticmethod', 'value_cannot_be_null.smali'))

    # exec the method
    res = emulator.exec_method('a', args={'p0': 1, 'p1': 1, 'p2': -1})
    assert res == "value cannot be null".encode('ascii')


@pytest.mark.parametrize(
    'p0,p1,p2,expected', [
        (1, 0, 0, 'MK'),
        (0, 1, 1, "Key is null or does not exist")
    ]
)
def test_full_static_class_with_init(p0, p1, p2, expected):
    """Test two successive calls: 
      - first on '<clinit>' for initializing static fields
      - second on 'a' for deciphering some string
    """
    emulator = smali.emulator.Emulator()
    emulator.load_class(get_file_path('completeclass', 'full_static_class.smali'))
    res = emulator.exec_method('<clinit>', args=None)
    res = emulator.exec_method(
        'a', args={'p0': p0, 'p1': p1, 'p2': p2}, 
        vm=emulator.vm  # need to propagate the vm because it contains 
                        # the static fields initialized from call to <clinit>
    )
    assert res == expected.encode('ascii')
