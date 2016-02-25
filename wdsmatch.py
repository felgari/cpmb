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

"""This script finds matches between the WDS catalog and a list of stars."""

import sys
import csv
import operator

from ctes import *

NUM_ARGS = 3
# SDSS has an all-sky precision of 70 mas and systematic errors of less than 
# 30 mas, this adds 0.1 s.
COORD_MARGIN = 0.00002778

# Columns of the WDS catalog.
WDS_NAME_COL = 0
WDS_RA_COL = 1
WDS_DEC_COL = 2

# Columns of the other catalog.
CAT_NAME_COL = 0
CAT_RA_DEC = [[1, 2], [8, 9]]

def in_range(val1, val2):
    """Check if the values received accomplished the criteria of proximity.
    
    Args:
        val1: First value to compare.
        val2: Second value to compare.
        
    """
    
    return val1 - COORD_MARGIN < val2 and val1 + COORD_MARGIN > val2

def check_match(wds_row, cat_row, matches):
    """Check if the stars in both rows match.
    
    Args:
        wds_row: Row of the WDS catalog.
        cat_row: Row of the second catalog.
        matches: List of matches.
        
    """
    
    matchFound = False
    
    try:
        
        # Get WDS RA and DEC values.
        wds_ra = float(wds_row[WDS_RA_COL])
        wds_dec = float(wds_row[WDS_DEC_COL])          
        
        # The catalog could contain more than one star per line. 
        # So try to find a match with any of them.
        for pair in CAT_RA_DEC:
            cat_ra = float(cat_row[pair[0]])
            cat_dec = float(cat_row[pair[1]])                      
            
            if in_range(cat_ra, wds_ra) and \
                in_range(cat_dec, wds_dec):
                
                matches.append([wds_row[WDS_NAME_COL], \
                                cat_row[CAT_NAME_COL]])
                
                break
            
    except ValueError as ve:
        print "ERROR %s: %s %s %s %s" % (ve, cat_row[CAT_RA_COL], \
                                         cat_row[CAT_DEC_COL], \
                                         wds_row[WDS_RA_COL], \
                                         wds_row[WDS_DEC_COL])

def write_matches(matches):
    """Saves the matches between the WDS catalog and the pairs to a file.
    
    Args:
        matches: List of matches.
        
    """
    
    print "Saving matches found to file '%s'" % MATCHES_FILENAME
    
    with open(MATCHES_FILENAME, "w") as fw:
    
        for m in matches:    
            
            fw.write("%s%s%s\n" % (m[0], CSV_DELIMITER, m[1]))            

def read_second_catalog(other_cat_file_name):
    """Read the second catalog
    
    Args:
        other_cat_file_name: Name of the file containing another catalog.
        
    """
    
    cat_list = []
    
    print "Reading catalog file: %s" % other_cat_file_name
    
    # Flatten the list of indexes with RA DEC values.
    CAT_RA_DEC_INDEXES = [item for sublist in CAT_RA_DEC for item in sublist]
    
    with open(other_cat_file_name, 'rb') as cat_f:
        
        cat = csv.reader(cat_f)
        
        try:
            for row in cat:
                new_row = []
                
                for i in range(len(row)):                    
                    if i in CAT_RA_DEC_INDEXES:
                        new_row.append(float(row[i]))
                    else:
                        new_row.append(row[i])
                    
                cat_list.append(new_row)
        
        except csv.Error:
            print "ERROR: reading file %s" % other_cat_file_name
            
    print "Read %d lines from file '%s'. Now sorting by RA and DEC." % \
        (len(cat_list), other_cat_file_name)
        
    # Sort the catalog.
    cat_list.sort(key=operator.itemgetter(CAT_RA_DEC_INDEXES[0], \
                                          CAT_RA_DEC_INDEXES[1]))             
            
    return cat_list

def match_catalogs(wds_file_name, other_cat_file_name):
    """Check if the pairs in catalog 2 are already in the WDS catalog.
    
    Args:
        wds_file_name: File containing the WDS catalog.
        other_cat_file_name: File containing another catalog of pairs.
        
    """
    
    matches = []
    
    # Read and sort the second catalog.
    sorted_catalog = read_second_catalog(other_cat_file_name)
            
    if len(sorted_catalog) > 0:        
        cat_index = 0
        
        cat_row = sorted_catalog[cat_index]
        cat_ra = float(cat_row[CAT_RA_DEC[0][0]])
        cat_dec = float(cat_row[CAT_RA_DEC[0][1]])
        
        print "Opening WDS file '%s' to find matches." % wds_file_name
    
        # Open the WDS catalog, already sorted, and look for matches.
        with open(wds_file_name, 'rb') as wds_f:
            
            wds_cat = csv.reader(wds_f)                        
            
            try:                                                       
                for wds_row in wds_cat:
                    
                    wds_ra = float(wds_row[WDS_RA_COL])
                    wds_dec = float(wds_row[WDS_DEC_COL])
                    
                    check_match(wds_row, cat_row, matches)
                    
                    # Read from second catalog when WDS RA is greater than 
                    # RA from second catalog and there is some item in
                    # second cat.
                    while ( ( wds_ra > cat_ra ) or \
                            (wds_ra >= cat_ra and wds_dec > cat_dec) ) and \
                        cat_index < len(sorted_catalog) - 1:
       
                        cat_index += 1
                 
                        cat_row = sorted_catalog[cat_index]   
                        cat_ra = float(cat_row[CAT_RA_DEC[0][0]])     
                        cat_dec = float(cat_row[CAT_RA_DEC[0][1]])                         
                        
                        check_match(wds_row, cat_row, matches)                           
            
            except csv.Error:
                print "ERROR: reading file %s" % wds_file_name
                
        print "Found %d matches" % len(matches)
        
        if len(matches) > 0:            
            write_matches(matches)

if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(match_catalogs(sys.argv[1], sys.argv[2]))
    else:
        print "ERROR: Wrong number of parameters. Use: "
        print "\t%s wds_file_name other_catalog_file_name" % sys.argv[0]