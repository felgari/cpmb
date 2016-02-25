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

"""Script to extract the objects in a given zone.
"""

import sys
import csv
from ctes import *
from common import *

NUM_ARGS = 4

def extract_zone(csv_file_name, ra, dec):
    """Calculate the proper motion of the objects and add it as a column.
    
    Args:
        csv_file_name: Name of the CSV file with the data.
        ra: Starting RA for the zone.
        dec: Starting DEC for the zone.
        
    Return:
        The output file created.
        
    """
    
    min_ra = float(ra) - ZONE_MARGIN 
    max_ra = float(ra) + RA_SIZE + ZONE_MARGIN 
    
    min_dec = float(dec) - ZONE_MARGIN 
    max_dec = float(dec) + DEC_SIZE + ZONE_MARGIN   
    
    print "RA between %.5g and %.5g DEC between %.5g and %.5g" % \
                 (min_ra, max_ra, min_dec, max_dec)   
    
    row_num = 0
    
    suffix = "_%s_%s.csv" % (ra, dec)
    
    out_file_name = csv_file_name.replace(".csv", suffix)
    
    print "Opening file for writing: %s" % out_file_name   
    
    try:    
        with open(out_file_name, 'w') as csv_out:   
            writer = csv.writer(csv_out, delimiter=CSV_DELIMITER)
        
            print "Opening file for reading: %s" % csv_file_name
            
            with open(csv_file_name, 'rb') as csv_in:
                reader = csv.reader(csv_in, delimiter=CSV_DELIMITER)
                
                for row in reader:
                    
                    write_row = False
                    
                    if row_num == 0:
                        write_row = True
                    else:
                        ra = get_float_value(row[RA_COL], row_num)
                        dec = get_float_value(row[DEC_COL], row_num)
                        
                        if ra > min_ra and ra < max_ra and \
                            dec > min_dec and dec < max_dec:
                            write_row = True
                        
                    if write_row:                           
                        writer.writerow([r.replace("...", "") for r in row])
                    
                    row_num += 1   
                        
    except IOError as ioe:
        print "ERROR: %s" % ioe  
        
    return out_file_name
        
if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(extract_zone(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print "ERROR: Wrong number of parameters. Use: %s input_file ra dec" % \
                      sys.argv[0]