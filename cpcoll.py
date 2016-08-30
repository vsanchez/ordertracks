#!/usr/bin/python3

import sys
import taglib
import argparse
import glob
import re
import os
import shutil 

def was_changed(srcfile,destfile):
    """Makes an attempt to determine if the file at the origin has not been
       changed... is not easy because in my collection they *have been* changed in ways
       that not require a recopy of the file. Specially if the program ordertracks.py has
       been used to modify the title...
       
       It still may fail to discover if the file is the same.. I have not investigated why yet.
    """
    
    src = taglib.File(srcfile)
    dest =taglib.File(destfile)
    
    if verbose: print(src.tags)
    if verbose: print(dest.tags)

    if 'ORDERTRACKS' in dest.tags.keys():
        if verbose: print("Destination had been processed by ordertracks.py")
        del dest.tags['ORDERTRACKS']
        title = dest.tags['TITLE'][0]
        title = title.split('- ',1)[1]
        dest.tags['TITLE'] = [title]
        
        # Apparently taglib does not store empty ID elements, so that the original file
        # can have an empty ID element and ordertrack.py will drop it while modifying the ID
        # the problem is that the original still has them. We need to delete them before doing the
        # comparison.
        
        
        empty_keys = [k for k,v in src.tags.items() if v==['']]
        for k in empty_keys:
            del src.tags[k]    
        
    if src.tags == dest.tags:
        # No change?
        if verbose: print("No aparent change.")
        return False
    else: 
        if verbose: print("There is a change.")
        return True

    

parser = argparse.ArgumentParser(description="Copies a collection of music files to a an USB drive.Only copies modified files.")
parser.add_argument('-s','--save',action='store_true',
                    help='modify the file. By default the program only performs a dry-run.')
parser.add_argument('-v','--verbose',action='store_true',
                    help='be more verbose')
parser.add_argument('srcdir',type=str,
                    help='directory where to look for files.')
parser.add_argument('destdir',type=str,
                    help='directory where to copy the files.')
args = parser.parse_args()

verbose = args.verbose
save = args.save

# The following hack is to make sure that the directory ends in the slash...
srcdir = args.srcdir
if srcdir[-1] != '/': 
    srcdir += '/'

destdir = args.destdir
if destdir[-1] != '/': 
    destdir += '/'
    
music = re.compile('^.*\.(mp3|flac)$') 

for musicfile in glob.iglob(args.srcdir+'**', recursive=True):
    
    if music.match(musicfile):
        if verbose: print(musicfile)
 
        destfile = destdir+musicfile[len(srcdir):]
 
        if not os.path.isfile(destfile):
            # Needs to copy the file, but first must check if the directory exists..
            if not os.path.isdir(os.path.dirname(destfile)):
                if save: os.makedirs(os.path.dirname(destfile))
            if save: shutil.copyfile(musicfile,destfile)
            
        else:
            # File already exists... are there changes withing both files?
            
            if was_changed(musicfile,destfile):
                if save: shutil.copyfile(musicfile,destfile)
                
# Now eliminate files in de repository that no longer are in the origin

if verbose: print("Eliminating deleted files in the source.")

for destfile in glob.iglob(destdir+'**', recursive=True):
    if music.match(destfile):
        origfile = srcdir+destfile[len(destdir):]
        if not os.path.isfile(origfile):
            if verbose: print("Removing this file")
            if save: os.remove(destfile)
            
 

                
            
            
