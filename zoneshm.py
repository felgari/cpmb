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

"""Script to plot a heat map of the zones showing the density of objects.
"""

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from ctes import *
from common import *

NUM_ARGS = 2

CSV_DELIMITER = ','

ZONE_NUM_COLS = 360/RA_SIZE
ZONE_NUM_ROWS = int(DEC_MAX + abs(DEC_MIN)) / DEC_SIZE

zones = [[0 for x in range(ZONE_NUM_COLS)] for x in range(ZONE_NUM_ROWS)]

def plot_heatmap():
    """Plot a heat map of the zones.
    """
    
    print "Matrix of %d rows by %d columns." % (len(zones), len(zones[0]))
    
    column_labels = [x for x in range(0, 360, RA_SIZE)] 
    row_labels = [ x for x in range(int(DEC_MIN), int(DEC_MAX), DEC_SIZE)]
    
    fig, ax = plt.subplots()
    
    data = np.array(zones)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    
    # put the major ticks at the middle of each cell
    ax.set_yticks(np.arange(data.shape[0]), minor=False)
    ax.set_xticks(np.arange(data.shape[1]), minor=False)
    
    ax.set_yticklabels(row_labels, minor=False)
    ax.set_xticklabels(column_labels, minor=False)
    
    plt.xticks(rotation=90) 
    
    plt.show() 

def get_pos_stats(csv_file_name):
    """Calculate the range of RA and DEC for the objects and count the number
    of objects is each zone used to divide the sky.
    The input file must use the CSV format.
    A list containing an item for each zone is used to store the counts.
    
    Args:
        csv_file_name: Name of the CSV file with the data.
    """
    
    ra_min = 9999.0
    ra_max = -9999.0
    dec_min = 9999.0
    dec_max = -9999.0
    
    row_num = 0
    
    print "Opening file: %s" % csv_file_name
    
    with open(csv_file_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=CSV_DELIMITER)
        
        for row in reader:
            
            # Ignore header.
            if row_num > 0:
                ra = get_float_value(row[RA_COL], row_num)
                
                if ra < ra_min:
                    ra_min = ra
                    
                if ra > ra_min:
                    ra_max = ra      
                    
                ra_index = int(ra / RA_SIZE) - 1         

                dec = get_float_value(row[DEC_COL], row_num)
                
                if dec < dec_min:
                    dec_min = dec
                    
                if dec > dec_max:
                    dec_max = dec  
                 
                dec_index = int((dec + abs(DEC_MIN)) / DEC_SIZE) - 1
                
                try:
                    zones[dec_index][ra_index ] += 1
                except IndexError:
                    print "dec %.5g dec_index %d ra %.5g ra_index %d" % \
                        (dec, dec_index, ra, ra_index)
                    
            row_num += 1                                                             
           
    print "Min RA: %.5g Max. RA: %.5g Min. DEC: %.5g Max. DEC: %.5g" % \
        (ra_min, ra_max, dec_min, dec_max)   
    
    plot_heatmap()

if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(get_pos_stats(sys.argv[1]))
    else:
        print "ERROR: Wrong number of parameters. Use: %s input_file_name" % \
        sys.argv[0]