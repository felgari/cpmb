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

"""Script to process an astronomical catalog of stars to look for those with 
common proper motion.
""" 

import sys
import mparser

from ctes import *
from extzone import extract_zone
from findcpmb import find_cpmb

def process_catalog_file(catalog_file_name):
    """Process the file containing the catalog of objects to find those 
    with common proper motion.
    
    First the catalog is divided into zones to distribute the checking of 
    the pairs found.
    The pairs are searched by zones.
    There is some overlapping between zones to avoid loosing pairs.
    
    Args:
        catalog_file_name: Name of the file with the catalog.
        
    """
    
    print "Processing catalog file: %s" % catalog_file_name
    
    for ar in range(RA_MIN, RA_MAX, RA_SIZE):
        for dec in range(int(DEC_MIN), int(DEC_MAX), DEC_SIZE):
            
            print "Processing AR %d DEC %d" % (ar, dec)
            
            out_file_name = extract_zone(catalog_file_name, ar, dec)
            
            cpmb_file = find_cpmb(out_file_name)

            print "Saved out file %s" % cpmb_file
            
    print "Finished the processing of the catalog file: %s" % catalog_file_name
    
def main(progargs):
    """Main function.
    
    Args:
        progargs: Program arguments already processed.

    """    
    
    process_catalog_file(progargs.file_name)
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    try:
        # Object to process the program arguments.
        progargs = mparser.ProgramArguments()
        
        sys.exit(main(progargs))   
    except mparser.ProgramArgumentsException as pae:
        print pae   