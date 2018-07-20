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

# stdlib
import os
import os.path

# 3d party
import pytest

# internals
from smali.source import get_source_from_file
from smali.parser import (
    extract_attribute_names,
    extract_methods,
)

@pytest.fixture
def filename():
    yield os.path.join(
        os.path.dirname(__file__),
        'completeclass',
        'static_obfuscated_parameters.smali'
    )

def test_read_attributes_from_class_file(filename):
    source_code = get_source_from_file(filename)
    identifier_list = [
        field_identifier
        for (field_identifier, field_type) in extract_attribute_names(source_code)
    ]
    assert all(x in identifier_list
               for x in ('l', 'o', 'p', 'q', 'r', 's', 't', 'u', 'x'))


def test_read_method_list_from_class_file(filename):
    source_code = get_source_from_file(filename)
    method_list = [method
                   for (method, input_types, output_types) in extract_methods(source_code)]
    assert all(x in method_list for x in ('$$d', '$$a', '<init>'))

