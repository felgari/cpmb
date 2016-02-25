#!/usr/bin/env python
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

"""Sort the WDS catalog by RA and DEC."""

import sys
import csv
import operator

ID_COL = 0
RA_COL = 1
DEC_COL = 2

OUT_FILE_PREFIX = 'ord_'

def process_file(csv_file_name):
    
    rows = []
    
    is_header =  True
    
    with open(csv_file_name, 'rb') as f:
        
        reader = csv.reader(f)
    
        try:
            for row in reader:
                # If it is not the header.
                if not is_header:
                
                    rows.append([row[ID_COL], float(row[RA_COL]), \
                                 float(row[DEC_COL])])
                else:
                    # Ignore the header.
                    is_header = False
        
        except csv.Error:
            print "ERROR: reading file %s" % csv_file_name  
            
    rows.sort(key=operator.itemgetter(RA_COL, DEC_COL))  
            
    output_file_name = OUT_FILE_PREFIX + csv_file_name
    
    previous_out_str = ''
    out_str = ''
    
    with open(output_file_name, "w") as fw:
                    
        for r in rows:   
            r_pro = [r[ID_COL], str(r[RA_COL]), str(r[DEC_COL])]
            
            out_str = ','.join(r_pro) + '\n'
            
            # Ignore duplicated rows.
            if previous_out_str != out_str:   
                fw.write(out_str)  
            
            previous_out_str = out_str

if __name__ == "__main__":
    
    process_file(sys.argv[1])
    
    