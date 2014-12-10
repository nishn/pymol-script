#!/usr/bin/env python
# coding: UTF-8
import sys
import os.path
from optparse import OptionParser

# check if the pymol module is installed
try :
    import pymol
except :
    sys.exit( "error : This script needs 'pymol' module. Please install PyMOL before running." )


def name_check( string, name ):
    if os.path.exists( string ):
        with open( string ) as f:
            return ( f.read(), os.path.basename(string) )
    else:
        return ( string, name )
    
def cartoon( filename, name ):
    pymol.finish_launching()
    pymol.cmd.read_pdbstr( *name_check( filename, name ) )

    pymol.cmd.hide( "everything" )
    pymol.cmd.show( "cartoon" )
    pymol.cmd.spectrum()

if __name__ == "__main__":

    # OptionParser
    def opt():
        # about this script
        parser = OptionParser( usage       = "%prog [options] PDB_FILE",
                               description = "Show the PDB_FILE in cartoon model using PyMOL." )

        ###### set options #######

        # parse arguments
        ( options, args ) = parser.parse_args()

        # check arguments
        if len( args ) != 1 :
            parser.error( "Incorrect number of arguments. "
                          "Just one PDB_FILE must be given. \n"
                          "\t\tTo show help message, use '-h or --help' option." )

        # check if "file" exists
        if not os.path.isfile( args[0] ) :
            sys.exit( "error : \"" + args[0] + "\" : no such file" )

        return ( options, args )

    ( options, args ) = opt()
    cartoon( args[0], None )
