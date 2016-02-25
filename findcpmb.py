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

"""Script to find stars with common proper motion.
The criteria used to select stars with common proper motion is taken from:
Halbwachs, J.L., 1986, “Common proper motion stars in the AGK3”.
Bull. Inf. Centre Donnees Stellaires, 30, p.129. 
"""

import sys
import os
import csv
import math
import numpy as np

from ctes import *

NUM_ARGS = 2

# 84" in decimal degrees.
ANG_DIST_DEC_DEG = 0.0233333333

# mas/yr-1
MIN_PM_MODULE = 50.0

MAX_PM_ERROR_PERCENT = 0.2

DEC_DEG_TO_MAS = (3600 * 1000) 
DEC_DEG_TO_RAD = 0.017453293

LN_0_05 = -2.995732274

def read_csv_data(csv_file_name):
    """Read data from a CSV file.
    
    Args:
        csv_file_name: Name of the CSV file.
        
    """
    
    data = []
    
    with open(csv_file_name, 'rb') as f:
        
        reader = csv.reader(f)
    
        try:
            for row in reader:
                data.append(row)
        
        except csv.Error:
            print "ERROR: reading file %s" % csv_file_name
            
    return data

def near_objects(star_a, star_b):
    """Indicates if both stars are close enough to be considered for common 
    proper motion.
    
    Args:
        star_a: Data of the star A.
        star_b: Data of the star B.
    
    """    
    
    ra_dif = star_a[RA_COL] - star_b[RA_COL]
    dec_dif = star_a[DEC_COL] - star_b[DEC_COL]
        
    sep_in_deg_dec = math.sqrt( math.pow(ra_dif, 2) + math.pow(dec_dif, 2) )
    
    return sep_in_deg_dec < ANG_DIST_DEC_DEG, sep_in_deg_dec

def low_pm_error(pm, pm_error):
    """Indicates if the proper motion value received has a low error.
    
    Args:
        pm: Proper motion value.
        pm_error: Proper motion error.
        
    """    
    
    return pm_error < pm * MAX_PM_ERROR_PERCENT 

def pm_reliability_criteria(star_a, star_b):
    """Applies a reliability criteria for the data of both stars.
    
    Args:
        star_a: Data of the star A.
        star_b: Data of the star B.
    
    """
    
    return low_pm_error(star_a[RA_PM_COL], star_a[PMRA_TOTERR_COL]) and \
        low_pm_error(star_a[DEC_PM_COL], star_a[PMDEC_TOTERR_COL]) and \
        low_pm_error(star_b[RA_PM_COL], star_b[PMRA_TOTERR_COL]) and \
        low_pm_error(star_a[DEC_PM_COL], star_a[PMDEC_TOTERR_COL])

def vector_module(ra_pm, dec_pm):
    """Calculates the module for the proper motion of a star.
    
    Args:
        ra_pm: RA proper motion.
        dec_pm: DEC proper motion.
        
    """
    
    return math.sqrt( math.pow(ra_pm, 2) + math.pow(dec_pm, 2) )

def pm_module_criteria(star_a_pm):
    """Applies criteria for the minimum value of the module of the proper motion.
    
    Args:
        star_a_pm: Proper motion of star A.
        
    """    

    return star_a_pm >= MIN_PM_MODULE 

def Halbwachs_first_criteria(star_a, star_b, sep_in_deg_dec):
    """Applies Halbwachs first criteria to find common proper motion stars.
    
    Args:
        star_a_pm: Star A data.
        star_b_pm: Star B data.
        sep_in_deg_dec: Separation of both stars in decimal degress.
        
    """    
        
    delta_pm_ra = star_a[RA_PM_COL] - star_b[RA_PM_COL]    
    delta_pm_dec = star_a[DEC_PM_COL] - star_b[DEC_PM_COL]
    
    # sigma calculation from Halbwachs (3).
    sigma_ra = math.sqrt( math.pow(star_a[PMRA_TOTERR_COL], 2) + \
                math.pow(star_b[PMRA_TOTERR_COL], 2) )
                
    sigma_dec = math.sqrt( math.pow(star_a[PMDEC_TOTERR_COL], 2) + \
                math.pow(star_b[PMDEC_TOTERR_COL], 2) )

    # From Halbwachs (9).
    return math.pow(delta_pm_ra, 2) < (-2 * sigma_ra * LN_0_05) \
        and math.pow(delta_pm_dec, 2) < (-2 * sigma_dec * LN_0_05)
    
def Halbwachs_second_criteria(star_a_pm, star_b_pm, sep_in_deg_dec):
    """Applies Halbwachs second criteria to find common proper motion stars.
    
    Args:
        star_a_pm: Proper motion of star A.
        star_b_pm: Proper motion of star B.
        sep_in_deg_dec: Separation of both stars in decimal degress.
        
    """
    
    sep_in_mas = sep_in_deg_dec * DEC_DEG_TO_MAS
    
    # From Halbwachs 3.
    return sep_in_mas / star_a_pm < 1000 and sep_in_mas / star_b_pm < 1000   

def get_numbers(data):
    """Get the data received as a list of numbers.
    The first item of the row is a number and the rest are converted to float.
    
    Args:
        data: data with values.
        
    """
        
    number_list = [data[0]] 
    
    number_list.extend([ float(x) for x in data[1:] ])
    
    return number_list

def get_column_values(row):
    """Get the data of the row as a string.
    The first item of the row is a string but the rest aren't so it is
    necessary to convert them to string.
    
    Args:
        row: Row with values.
        
    """
    
    str_values = [ str(x) for x in row[1:] ]
    
    return "%s%s%s" % (row[0], CSV_DELIMITER, CSV_DELIMITER.join(str_values))

def save_candidates(candidates, csv_file_name):
    """Save the candidates found to a file in CSV format.
    
    Args:
        candidates: List of candidates.
        csv_file_name: Name of the file with the initial list of stars.
    
    """
    
    output_file_name= "NO FILE WITH CANDIDATES"
    
    if not candidates:
        print "No candidate pair found in file: %s" % csv_file_name
    else:
        path, file = os.path.split(csv_file_name)
        
        output_file_name = os.path.join(path, OUT_FILE_PREFIX + file)
        
        print "Saving candidates to %s" % output_file_name
        
        with open(output_file_name, "w") as fw:
        
            columns = CSV_DELIMITER.join(NAMES_COLS_OF_INTEREST)
        
            fw.write("%s%s%s\n" % (columns, CSV_DELIMITER, columns))
        
            for c in candidates:
                
                columns_a = get_column_values(c[0])
                columns_b = get_column_values(c[1])
                
                fw.write("%s%s%s\n" % (columns_a, CSV_DELIMITER, columns_b))
                
    return output_file_name

def find_cpmb(csv_file_name):
    """Find stars with common proper motion.
    The stars are received in a file in CSV format.
    Only some columns are used for the calculations.
    Each star is compared with all the stars that follow to find the matches.
    
    Args:
        csv_file_name: CSV file with the list of stars.
        
    """
    
    # To store the candidates with common proper motion.
    candidates = []
    
    data = read_csv_data(csv_file_name)   
    
    for i in range(1, len(data)):
        
        star_a = get_numbers(data[i])
        
        star_a_pm = vector_module(star_a[RA_PM_COL], star_a[DEC_PM_COL])
        
        # Proper motion vector_module criteria for star A.
        if pm_module_criteria(star_a_pm):
        
            for j in range(i+1, len(data)):
                
                star_b = get_numbers(data[j])
                
                star_b_pm = vector_module(star_b[RA_PM_COL], star_b[DEC_PM_COL])
                
                # Proper motion vector_module criteria for star B.
                if pm_module_criteria(star_b_pm):
                
                    near, sep_in_deg_dec = near_objects(star_a, star_b)
                    
                    # Separation criteria and proper motion reliability.
                    if near and pm_reliability_criteria(star_a, star_b) and \
                        Halbwachs_second_criteria(star_a_pm, \
                                                  star_b_pm, \
                                                  sep_in_deg_dec):
                    
                        if Halbwachs_first_criteria(star_a, star_b, \
                                                    sep_in_deg_dec):
                            candidates.append([star_a, star_b])
            
    output_file_name = save_candidates(candidates, csv_file_name)
    
    return output_file_name

if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(find_cpmb(sys.argv[1]))
    else:
        print "ERROR: Wrong number of parameters. Use: %s input_file_name" % \
        sys.argv[0]