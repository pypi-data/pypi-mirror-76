# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:01:31 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2020  Shane Jaroch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

try:
    from .__sha__ import __sha__
except ImportError as e:
    __sha__ = "UNKNOWN"

__title__ = "nutra"
__version__ = "0.1.0.dev14"
__sha__ = __sha__
__author__ = "Shane Jaroch"
__license__ = "GPL v3"
__copyright__ = "Copyright 2018-2020 Shane Jaroch"
