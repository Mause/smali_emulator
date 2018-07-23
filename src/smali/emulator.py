# -*- coding: utf-8 -*-
# This file is part of the Smali Emulator.
#
# Copyright(c) 2016 Simone 'evilsocket' Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 3 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
from __future__ import print_function

import re
import sys
import time
import warnings

import smali
import smali.javaclass

from smali.opcodes import OpCode
from smali.vm import VM
from smali.source import Source, get_source_from_file
from smali.preprocessors import (
    PackedSwitchPreprocessor,
    TryCatchPreprocessor,
    ArrayDataPreprocessor,
)


class Stats(object):
    """Statistics about the running process."""
    def __init__(self, vm):
        self.opcodes = len(vm.opcodes)
        self.preproc = 0
        self.execution = 0
        self.steps = 0

    def __repr__(self):
        return (
            "opcode handlers    : {}\n"
            "preprocessing time : {} ms\n"
            "execution time     : {} ms\n"
            "execution steps    : {}\n"
        ).format(self.opcodes, self.preproc, self.execution, self.steps)


class Emulator(object):
    """Global Emulator class. Represent a complete virtual machine.

    Instanciate this if you want to do some work on the smali file."""
    def __init__(self, **kwargs):
        # Code preprocessors.
        self.preprocessors = [
            TryCatchPreprocessor,
            PackedSwitchPreprocessor,
            ArrayDataPreprocessor
        ]

        self.opcodes = []  # Opcodes handlers.
        for op_code_symbol in [
            entry for entry in dir(smali.opcodes) if entry.startswith('op_')
        ]:
            self.opcodes.append(getattr(smali.opcodes, op_code_symbol)())

        self.vm = kwargs.get('vm') or VM(self)           # Instance of the virtual machine.
        self.source = kwargs.get('source')               # Instance of the source file.
        self.stats = kwargs.get('stats') or Stats(self)  # Instance of the statistics object.
        self.javaclass = javaclass.JavaClass(kwargs.get('filename')) if kwargs.get('filename') else None

    def __preprocess(self):
        """
        Start the preprocessing phase which will save all the labels and their line index
        for fast lookups while jumping and will pre parse all the try/catch directives.
        """
        next_line = None
        self.source.lines = [line.strip() for line in self.source.lines]
        for index, line in enumerate(self.source.lines):
            # we're inside a block which was already processed
            if next_line is not None and index <= next_line:
                next_line = None if index == next_line else next_line
                continue

            # skip empty lines
            elif line == '':
                continue

            elif line[0] == ':':  # we've found something to preprocess
                # loop each preprocessors and search for the one responsible to parse this line
                # TODO: refactor this block. This is a dirty way to do the branching.
                # TODO: It should use a dictionary or  something like that.
                for preproc in self.preprocessors:
                    if preproc.check(line):
                        next_line = preproc.process(self.vm, line, index, self.source.lines)
                        break
                else:
                    self.vm.labels[line] = index

    def __parse_line(self, line):
        # Search for appropriate parser.
        for parser in self.opcodes:
            if parser.parse(line, self.vm):
                return True

        return False

    @staticmethod
    def __should_skip_line(line):
        """
        Helper method used to determine if a line must be skipped/ignored.
        :param line: The line to check.
        :return: True if the line can be ignored, otherwise False.
        """
        return line == "" or line[0] == '#' or line[0] == ':' or line[0] == '.'

    def fatal(self, message):
        """
        Display an error message, the current line being executed and quit.
        :param message: The error message to display.
        """
        print("\n-------------------------")
        print("Fatal error on line %03d:\n" % self.vm.pc)
        print("  %03d %s" % (self.vm.pc, self.source[self.vm.pc - 1]))
        print("\n%s" % message)
        sys.exit()

    def run_file(self, filename, args={}, trace=False):
        warnings.warn("This feature is deprecated, use load_class and exec_method instead",
                      DeprecationWarning)
        return self.run(get_source_from_file(filename), args, trace)

    def run_source(self, source_code, args={}, trace=False):
        warnings.warn("This feature is deprecated, use load_class and exec_method instead",
                      DeprecationWarning)
        return self.run(Source(lines=source_code), args, trace)

    def load_class(self, filename, trace=False):
        self.javaclass = smali.javaclass.JavaClass(filename)

    def exec_method(self, method_name, args=None, trace=False, vm=None):
        """Exec the method given the method_name and a list of arguments from
        current javaclass."""
        arg_length = len(args) if args else 0

        # TODO: check input argument type here
        candidate_methods = [
            self.javaclass.methods[(method_name, input_types, output_type)]
            for method, input_types, output_type in self.javaclass.methods 
            if method == method_name and arg_length == len(input_types)
        ]

        # If the following assert fails, it means that we must refine the 
        # search by matching the type of the input arguments with the input signature
        # of the method being executed.
        assert len(candidate_methods) == 1, "Too much methods for this number of arguments"
        method = candidate_methods[0]
        result = self.run(method, args=args, trace=trace, vm=vm)
        backup_vm = self.vm
        self.vm = VM(self)  # instanciate a new VM because we are on a new frame
        local_var_name = re.compile('(p|v)\d+')
        self.vm.variables.update(
            {k: v for k, v in backup_vm.variables.items() if not local_var_name.match(k)}
        )
        return result

    def preproc_source(self, source_object=None):
        """Preprocess labels and try/catch blocks for fast lookup."""
        self.source = self.source or source_object
        s = time.time() * 1000
        self.__preprocess()
        e = time.time() * 1000
        self.stats.preproc = e - s

    def run(self, source_object, args=None, trace=False, vm=None):
        """Load a smali file and start emulating it.

        :param source_object: A Source() instance containing the source code to run.
        :param args: A dictionary of optional initialization variables for the VM, used for arguments.
        :param trace: If true every opcode being executed will be printed.
        :return: The return value of the emulated method or None if no return-* opcode was executed.
        """
        OpCode.trace = trace
        self.source = source_object
        self.vm = VM(self) if not vm else vm
        self.stats = Stats(self)

        args = {} if not args else eval(args) if not isinstance(args, dict) else args
        self.vm.variables.update(args)
        self.preproc_source(self.source)

        # Loop each line and emulate.

        s = time.time() * 1000
        while self.vm.stop is False and self.source.has_line(self.vm.pc):
            self.stats.steps += 1
            line = self.source[self.vm.pc]
            self.vm.pc += 1

            if self.__should_skip_line(line):
                continue

            elif self.__parse_line(line) is False:
                self.fatal("Unsupported opcode.")

        e = time.time() * 1000
        self.stats.execution = e - s

        return self.vm.return_v


class FrameEmulator(Emulator):
    """Emulator Instance intended to run internal method of a class."""
    pass

