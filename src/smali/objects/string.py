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

import struct

class String:
    """Reproduce the behaviour of the java/lang/String class"""
    @staticmethod
    def name():
        return 'java.lang.String'

    @staticmethod
    def methods():
        """A dict containing the list of available methods for the class."""
        return {
            'new-instance': String.new_instance,
            '<init>([C)V': String.init_from_char_array,
            '<init>([BI)V': String.init_from_byte_array_and_code,
            'charAt(I)C': String.charat,
            'toCharArray()[C': String.tochararray,
            'intern()Ljava/lang/String;': String.repr_intern,
            'valueOf([CII)Ljava/lang/String;' :String.valueof,
            'length()I': String.length,
            'substring(II)Ljava/lang/String;' : String.ssubs,
        }

    @staticmethod
    def repr_intern(vm, this, args):
        return str(vm[this])

    @staticmethod
    def new_instance():
        return ""

    @staticmethod
    def init_from_char_array(vm, this, args):
        vm[this] = "".join(vm[args[0]])

    @staticmethod
    def init_from_byte_array_and_code(vm, this, args):
        vm[this] = "".join(struct.pack('>b', x) for x in vm[args[0]])
        return vm[this]

    @staticmethod
    def charat(vm, this, args):
        idx = vm[args[0]]
        obj = vm[this]
        vm.return_v = obj[idx]

    @staticmethod
    def tochararray(vm, this, args):
        vm.return_v = list(vm[this])

    @staticmethod
    def length(vm, this, args):
        vm.return_v = len(vm[this])

    @staticmethod
    def valueof(vm,this,args):
        v = "".join(vm[this])
        vm.return_v = v[int(vm[args[0]]):int(vm[args[1]])]

    @staticmethod
    def ssubs(vm,this,args):
        vm.return_v = vm[this][int(vm[args[0]]):int(vm[args[1]])]

