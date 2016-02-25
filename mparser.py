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

"""Process the program arguments received by the main function.

Define the arguments available, check for its correctness and coherence, 
and provides these arguments to other modules. 
"""

import argparse
import logging

class ProgramArgumentsException(Exception):
    
    def __init__(self, msg):
        
        self._msg = msg
        
    def __str__(self):
        return self._msg

class ProgramArguments(object):
    """Encapsulates the definition and processing of program arguments.
    
    """
    
    DEFAULT_LOG_LEVEL_NAME = logging.DEBUG
    DEFAULT_LOG_FILE_NAME = "log.txt"    
    
    FIT_FORMAT_FILE = "FIT"
    FIT_FORMAT_FILE = "CSV"
    
    # Error messages related to parameters coherence.
    NO_FILE_NAME_PROVIDED = "The name of the file that contains the catalog " \
        "must be provided."                       
    
    def __init__(self):
        """Initializes parser. 
        
        Initialization of variables and the object ProgramArguments 
        with the definition of arguments to use.

        """               
            
        # Initialize arguments of the parser.
        self.__parser = argparse.ArgumentParser()  
        
        self.__parser.add_argument("-f", dest="f", metavar="file_name",
                                   help="Name of the file with the catalog.")            
        
        self.__parser.add_argument("-ff", dest="ff", metavar="file_format",
                                   help="Format of the catalog file.")                     
                
        self.__parser.add_argument("-l", metavar="log_file", dest="l",
                                   help="File to save the log messages.") 
        
        self.__parser.add_argument("-v", metavar="log_level", dest="v",
                                   help="Level of the log to generate.")   
        
        self.__args = self.__parser.parse_args()

        if not self.file_name_provided:
            raise ProgramArgumentsException(ProgramArguments.NO_FILE_NAME_PROVIDED) 
        
    @property    
    def file_name_provided(self): 
        return self.__args.f is not None           
        
    @property
    def file_name(self):
        return self.__args.f
    
    @property    
    def file_format_provided(self): 
        return self.__args.ff is not None    
        
    @property    
    def file_format_is_fit(self):        
        return self.__args.ff == ProgramArguments.FIT_FORMAT_FILE
    
    @property    
    def file_format_is_csv(self):        
        return self.__args.ff == ProgramArguments.CSV_FORMAT_FILE    
    
    @property    
    def log_file_provided(self): 
        return self.__args.l is not None      
    
    @property
    def log_file_name(self):        
        if not self.log_file_provided:
            lfn = ProgramArguments.DEFAULT_LOG_FILE_NAME
        else:
            lfn = self.__args.l
            
        return lfn     

    @property
    def log_level_provided(self): 
        return self.__args.v is not None     
    
    @property
    def log_level(self):
        if not self.log_file_provided:
            lln = ProgramArguments.DEFAULT_LOG_LEVEL_NAME
        else:
            lln = self.__args.v
            
        return lln                                     
 
    def print_usage(self):
        """Print arguments options.
        
        """
                
        self.__parser.print_usage()     
        
    def print_help(self):
        """Print help for arguments options.
        
        """
                
        self.__parser.print_help()     