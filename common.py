# -*- coding: utf-8 -*-

# Copyright (c) 2016 Felipe Gallego. All rights reserved.
#
# This file is part of ycas: https://github.com/felgari/cpmb
#
# This is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Common functions used is several modules.
"""

def get_float_value(str_val, row_num):
    
    val = 0.0
    
    pos = str_val.find('...')
    
    if pos > 0:
        str_val = str_val[:pos]  
          
    try:
        val = float(str_val)                    
    except ValueError:
        print "Error in value: %s in row %d" % (str_val, row_num)   
        
    return val 