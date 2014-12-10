#!/usr/bin/env python
import os.path
import sys
from optparse import OptionParser

# check if the pymol module is installed
try :
    import pymol
except :
    sys.exit( "error : This script needs 'pymol' module. Please install pymol before running." )

######################################## function ###########################################

# make CA model
def ca( mode, with_separate, filename ):
    pdbdat = ""             # PDB data string
    bonds  = []             # a list consists of pairs of connected CA atoms
    last   = 0              # residue number of last atom
    resnum = 0              # residue number of focus atom

    # open the PDB_FILE and read data
    for line in open( filename, 'r' ).readlines() :
        
        # if not ATOM line or CA atom
        if line[0:4] != 'ATOM' or line[12:16] != " CA ":
            continue

        
        # set residue number
        if with_separate:               # if separete mode       : resnum is the very number in PDB_FILE
            resnum  = int(line[22:26])
        else:                           # or if continuous mode  : resnum is a count from the first CA
            resnum += 1

        
        # add pdb line
        pdbdat += line[0:22] + ( '%4d' % resnum ) + line[26:]
        
        
        # add bonds
        if last + 1 == resnum:
            bonds.append( ( str(last) + "/CA", str(resnum) + "/CA" ) )

        # update last residue number
        last = resnum

    # launch pymol
    pymol_argv = [ 'pymol', '-q' ]
    
    pymol.finish_launching()
    pymol.cmd.read_pdbstr( pdbdat, os.path.basename( filename ) ) 
    pymol.cmd.hide( 'everything' )

    # set bond information
    if mode == "stick" :
        for bond in bonds :
            pymol.cmd.bond( bond[0], bond[1] )
    else :
        pymol.cmd.set( "cartoon_trace", 1 )

    # display structure in 'mode'
    pymol.cmd.show( mode )

########################################## main ##############################################
if __name__ == "__main__":
    # OptionParser
    def opt() :
        # set an explanation of this program
        usage  = "%prog [options] PDB_FILE"
        dscrpt = ( "Show the structure of the  PDB_FILE by CA backbone using PyMOL."
                   "PyMOL needs to be installed." )
        parser = OptionParser( usage = usage, description = dscrpt )

        # set options
        
        # cartoon mode
        parser.add_option( "-c", "--cartoon", dest = "mode", default = "stick",
                           action = "store_const", const = "cartoon",
                           help = "Display in CA trace cartoon mode [ default : stick mode ]" )
        
        # Connect separate atoms or not
        parser.add_option( "-s", "--separate", default = False, action = "store_true",
                           help = "Do not connect discontinuous CA atoms. If not specified, "
                           "[ default : force connect distant CA atoms ]" )
        
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

            
        return [ options.mode, options.separate, args[0] ]
    

    # get options and Display in PyMOL
    ca( *opt() )

    # colorize the structure
    # blue : N-terminus
    # red  : C-terminus
    pymol.cmd.spectrum()

