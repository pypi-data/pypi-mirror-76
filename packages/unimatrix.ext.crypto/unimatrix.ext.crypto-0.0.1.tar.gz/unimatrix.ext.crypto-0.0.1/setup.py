#!/usr/bin/env python3
#
# Copyright (C) 2019-2020 Cochise Ruhulessin
#
# This file is part of unimatrix.ext.{{ pkg_name }}.
#
# unimatrix.ext.{{ pkg_name }} is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# unimatrix.ext.{{ pkg_name }} is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unimatrix.ext.{{ pkg_name }}.  If not, see <https://www.gnu.org/licenses/>.
import json
import os
import sys
from setuptools import find_namespace_packages
from setuptools import setup


version = str.strip(open('unimatrix/ext/crypto/VERSION').read())


setup(
    name='unimatrix.ext.crypto',
    version=version,
    packages=find_namespace_packages(),
    include_package_data=True,
    **json.loads((open('unimatrix/ext/crypto/package.json').read()))
)
