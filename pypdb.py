#!/usr/bin/env python
import os.path
import sys
import urllib2
from optparse import OptionParser

# check if the pymol module is installed
try :
    import pymol
except :
    sys.exit( "error : This script needs 'pymol' module. Please install PyMOL before running." )

# import other modules
import pym
import pyca



def download_pdb( pdb_id ):
    PDBURL = "http://www.rcsb.org/pdb/download/downloadFile.do"
    optstr = "fileFormat=pdb&compression=NO&structureId=" + pdb_id

    try :
        pdb = urllib2.urlopen( PDBURL + "?" + optstr ).read()
    except urllib2.URLError :
        sys.exit( "error : PDB ID " + pdb_id + " not found" )
        
    return ( pdb, pdb_id )

if __name__ == "__main__":
    def opt():
        # about this script
        parser = OptionParser( usage       = "%prog [options] PDB_ID",
                               description = "Download PDB_ID structure file from www.rcsb.org "
                               "and show as cartoon or CA trace using PyMOL" )

        ###### set options #######
        parser.add_option( "-c", "--ca", dest = "ca", default = False,
                           action = "store_true",
                           help = "Show the structure in CA trace [ default : cartoon ]" )

        
        # parse arguments
        ( options, args ) = parser.parse_args()
        
        # check arguments
        if len( args ) != 1 :
            parser.error( "Incorrect number of arguments. "
                          "Just one PDB_ID must be given. \n"
                          "To show help message, use '-h or --help' option." )
            
        # if the length of pdb_id is not 4 ( if invalid pdb_id )
        if len( args[0] ) != 4 :
            parser.error( "PDB ID must consist of 4 charactors." )

        return ( options, args )

    
    ( options, args ) = opt()
    if options.ca:
        pyca.ca( "stick", True, *download_pdb( args[0] ) )
    else:
        pym.cartoon( *download_pdb( args[0] ) )
        
