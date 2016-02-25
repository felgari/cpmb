#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Felipe Gallego. All rights reserved.
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

"""Script to convert the values of all the pairs found in the format required
for RA and DEC. 
"""

import os
import fnmatch
import csv
from operator import itemgetter
from ctes import *

def find_files(pattern, path):
    
    list_of_files = []
    
    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                list_of_files.append(os.path.join(root, name))
                
    print "Found %d files" % len(list_of_files)
    
    return list_of_files

def dec_to_deg(dec_val, is_ra = False):
    """Convert decimal degrees to RA in hours and DEC in sexagesimal 
    
    Args:
        dec_val: Decimal degrees value.
        is_ra: Indicates if the value received is a RA value.
    """
    
    return dec_val
    
    val = dec_val
    
    # RA is converted from 360 to 24.
    if is_ra:
        val = dec_val / 15
        
    deg = int(val)
    min = int(( val - float(deg) ) * 60)
    sec = ( val - float(deg) - ( float(min) / 60 ) ) * 3600
    
    return "%d:%d:%.6f" % (deg, min, sec) 

def convert_row_values(row, second_star_pos):
    """Process a row to convert its values.
    
    Args:
        row: The row with the values to convert.
        second_star_pos: The initial position for the values of the second star.
        
    """
    ra_deg_1 = dec_to_deg(float(row[RA_COL]), True)
    
    dec_deg_1 = dec_to_deg(float(row[DEC_COL]))
    
    ra_deg_2 = dec_to_deg(float(row[second_star_pos + RA_COL]), 
        True)
    
    dec_deg_2 = dec_to_deg(float(row[second_star_pos + DEC_COL]))
    
    new_row = [row[ID_COL], ra_deg_1, dec_deg_1, 
        row[RA_PM_COL], row[DEC_PM_COL], 
        row[PMRA_TOTERR_COL], row[PMDEC_TOTERR_COL], 
        row[second_star_pos + ID_COL], ra_deg_2, dec_deg_2, 
        row[second_star_pos + RA_PM_COL], 
        row[second_star_pos + DEC_PM_COL], 
        row[second_star_pos + PMRA_TOTERR_COL], 
        row[second_star_pos + PMDEC_TOTERR_COL]]
    
    return new_row

def convert_files(files):
    """Process a set of files to convert decimal degrees to the conventional 
    values of hours for RA and sexagesimal for DEC.
    Each row in the input file must contain sequentially the columns for two
    stars, so in each row two AR and DEC values are converted. The middle of
    the row indicates the initial position of the values for the second star.
    
    Args:
        files: List of files to process.
    """
    
    compiled_rows = []
    
    # Compìle the rows.
    for f in files:   
        
        print "Processing file: %s" % f
             
        with open(f, 'rb') as csv_in:
                reader = csv.reader(csv_in, delimiter=CSV_DELIMITER)
                
                # Skip header but use it to get the initial position for the 
                # values of the second star.
                row = next(reader, None)
                
                second_star_pos = len(row) / 2
                
                # Convert AR and DEC for each row.
                for row in reader:
                    new_row = convert_row_values(row, second_star_pos)                                      
              
                    compiled_rows.append(new_row)
    
    # Sort the rows by the identifiers of both stars.
    sorted_compiled_rows = sorted(compiled_rows, key=itemgetter(0, second_star_pos))
    
    # Remove duplicates. As the zones have are overlapped, some pairs could be
    # repeated.
    final_compiled_rows = []
    
    for i in range(0, len(sorted_compiled_rows) - 1):
        curr = sorted_compiled_rows[i]
        nxt = sorted_compiled_rows[i + 1]
        
        # If current row is the same that next one, ignore current row.
        if curr[ID_COL] != nxt[ID_COL] or \
            curr[second_star_pos + ID_COL] != nxt[second_star_pos + ID_COL]:
            final_compiled_rows.append(curr)
    
    # In any case the last row must be added.
    final_compiled_rows.append(sorted_compiled_rows[-1])
    
    print "Writing output file."
    
    # Write the converted rows.
    with open(CONVERTED_FILE_OUTPUT, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=CSV_DELIMITER)   
        
        for cr in final_compiled_rows:
            writer.writerow(cr)  
              
    return compiled_rows      

if __name__ == "__main__":
    
    # Look for the files in current path with the appropriate file format.
    files = find_files(OUT_FILE_PREFIX + "*", os.getcwd())
    
    # All the files found are processed.
    convert_files(files)