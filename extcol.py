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

"""Script to extract the columns to use from a file containing the complete
catalog.
"""

import sys
from ctes import *

NUM_ARGS = 2

DATA_DELIMITER = '|' 

def process_text_file(text_file_name):
    """Process the data of the catalog to generate a output file containing
    only the columns of interest.
    
    The input file must use a text format with columns delimited by a separator.
    The output file is saved in CSV format.
    
    Args:
        text_file_name: Name of the text file containing the catalog.
        
    """
    
    num_rows = 0
    
    print "Opening text file for reading: %s" % text_file_name
    
    out_file_name = text_file_name.replace('.txt', '.csv')
    
    if out_file_name != text_file_name:
    
        try:        
            print "Opening file for writing: %s" % out_file_name
            
            out_file = open(out_file_name, 'w')
            
            with open(text_file_name, 'rb') as fr:
                for line in fr:
                    
                    line_stripped = line.strip()        
    
                    if line_stripped[0] == DATA_DELIMITER:
                        data_line = line_stripped[1:-1].strip()
                        
                        row = data_line.split(DATA_DELIMITER)
                        
                        row_filtered = [row[i].strip() for i in COLS_OF_INTEREST]
                        
                        out_line = CSV_DELIMITER.join(row_filtered)
                        
                        out_file.write(out_line)
                        
                        out_file.write("\n")
                        
                        num_rows += 1
                        
            out_file.close()
            
            print "Process finished, %d rows saved." % num_rows
        
        except IOError as ioe:
            print "ERROR: %s: Opening text file: %s" % (ioe, text_file_name)  
            
    else:
        print "ERROR: Input file has the same name that output file must have."

if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(process_text_file(sys.argv[1]))
    else:
        print "ERROR: Wrong number of parameters. Use: %s input_file_name" % \
                      sys.argv[0]