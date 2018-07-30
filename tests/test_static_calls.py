# -*- coding: utf-8 -*-
# This file is part of the Smali Emulator.
#
# Copyright(c) 2016-2018 Simone 'evilsocket' Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# Copyright(c) 2018- David Kremer, courrier@david-kremer.fr
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

from __future__ import unicode_literals

# 3d party
import pytest

import smali.classloader
import smali.emulator

# internal
from .conftest import (
    static_method_calls,
)

@pytest.mark.parametrize(
    'filepath, expected_result, input_source',
    static_method_calls()
)
def test_all_static_files(filepath, expected_result, input_source):
    test_params = eval(expected_result)
    expected_result = test_params.pop('ret')
    cl = smali.classloader.ClassLoader()
    cl.load_class(filepath)
    emu = smali.emulator.Emulator(class_loader=cl)
    result = emu.run_source(input_source, args=test_params)
    assert expected_result == result.internal

