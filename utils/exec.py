#!/usr/bin/env python

from __future__ import unicode_literals

"""Exec Smali Files.

Usage:
    exec.py -i File.smali -m methodName [-p methodParameters]

Options:
    -h --help        Show this screen.
    -i <filename>    The smali file to execute.
    -m <method>      The name of the method to execute.
    -p <parameters>  A list of parameters to give as arguments.
                     If not provided, the script will introspect the method
                     and give insights about what parameters are expected.
"""

from docopt import docopt
import smali.emulator
import ast


def main(arguments):
    filename = arguments.get('-i')
    parameters = arguments.get('-p')
    parameters = ast.literal_eval(parameters) if parameters else {}
    emu = smali.emulator.Emulator()
    result = emu.run_file(filename, parameters)
    print(result)


if __name__ == '__main__':
    main(docopt(__doc__))
