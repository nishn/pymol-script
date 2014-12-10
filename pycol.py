#!/usr/bin/env python
# coding: UTF-8
import sys
from optparse import OptionParser

# check if the pymol module is installed
try :
    import pymol
except :
    sys.exit( "error : This script needs 'pymol' module. Please install pymol before running." )

    
# import other pymol modules
import pyca

def colorize( start, end, col ):
    select = col
    pymol.cmd.select( select, "resi %d:%d" % (start, end) )
    pymol.cmd.color(  col, select )
    
if __name__ == "__main__":
    
    # OptionParser
    def opt():
        # about this script
        parser = OptionParser( usage       = "%prog [options] PDB_FILE",
                               description = "Colorize the specified region of the structure "
                               "with a specified color." )

        ###### set options #######

        # first resnum
        parser.add_option( "-f", "--first", dest = "first", default = None,
                           action = "store", type = "int",
                           help = "Residue number of the first residue in the region to be colorized." )

        # last resnum
        parser.add_option( "-l", "--last", dest = "last", default = None,
                           action = "store", type = "int",
                           help = "Residue number of the last residue in the region to be colorized." )

        # number of residues
        parser.add_option( "-n", "--num", dest = "num", default = None,
                           action = "store", type = "int",
                           help = "The count of residues in the region to be colorized." )

        # color
        parser.add_option( "-c", "--color", dest = "color", default = "white",
                           action = "store", type = "string",
                           help = "Name of the color to use. [ default : white ]" )

        
        # parse arguments
        ( options, args ) = parser.parse_args()

        # check arguments
        if len( args ) != 1 :
            parser.error( "Incorrect number of arguments. "
                          "Just one PDB_FILE must be given. \n"
                          "\t\tTo show help message, use '-h or --help' option." )
        if options.first == None or ( options.last == None and options.num == None ):
            parser.error( "Invalid argument. \n"
                          "'-f' and '-l' or '-c' must be specified.\n"
                          "To show help message, use '-h or --help' option." )
        return ( options, args )

    def opt_parse( options ):
        last = options.last if options.last != None else options.first + options.num
        return ( options.first, last, options.color )

    ( options, args ) = opt()
    pyca.ca( "stick", True, args[0] )
    colorize( *opt_parse( options ) )
