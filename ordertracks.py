#!/usr/bin/python3

import sys
import os
import taglib
import argparse
import glob
import re

def number_to_letter(n):
    return chr(int(n) + ord('A')-1)

def get_track_number(id):
    track_number = ''
    if 'TRACKNUMBER' in id.tags.keys():
        if id.tags['TRACKNUMBER']: 
            track_number = id.tags['TRACKNUMBER'][0]
        
            if not track_number.isdigit():
            
                # 
                # Get the first number we find in the string...
                #
                track_number = track_number.partition('/')[0]
                if not track_number.isdigit():
                    lista = [s for s in track_number.split() if s.isdigit()]
                    print(track_number,lista)   
                    track_number=lista[0]
            if int(track_number) < 10 and track_number[0] != '0':
                track_number = '0'+track_number

    return track_number        
    
def get_disc_letter(id):
    letter = ''
    if 'DISCNUMBER' in id.tags.keys():
        if id.tags["DISCNUMBER"]: 
            disc_number = id.tags["DISCNUMBER"][0]
        
            if not disc_number.isdigit():

                # If the disc number is in the form n/m take only n
                
                disc_number = disc_number.partition('/')[0]
            
            if not disc_number.isdigit():  # Here we give up.
                return letter
            letter = number_to_letter(disc_number)

    return letter  

def get_title(id):
    title = ''
    if 'TITLE' in song.tags.keys():  
        if id.tags["TITLE"]:
            title = song.tags["TITLE"][0]
    return title    

parser = argparse.ArgumentParser(description="Change song names so that alphabetic listing coincides with intended order.")
parser.add_argument('-s','--save',action='store_true',
                    help='modify the file. By default the program only performs a dry-run.')
parser.add_argument('-v','--verbose',action='store_true',
                    help='be more verbose')
parser.add_argument('-i','--ignore-stamp',action='store_true',
                    help='ignore "already modified" stamp in file. Will reprocess file.')
parser.add_argument('path',type=str,
                    help='directory where to look for files.')
args = parser.parse_args()

rootdir = args.path
do_save = args.save
verbose = args.verbose
ignore_stamp = args.ignore_stamp



count = 0
modified = 0

# Put here all terminations for music files (that support ID tags)

music = re.compile('^.*\.(mp3|flac|MP3|FLAC)$')

for musicfile in glob.iglob(rootdir+'/**', recursive=True):

    if music.match(musicfile):
        count+=1
        song = taglib.File(musicfile)
        print("Examining: ",musicfile)
        if verbose: print("tags: ",song.tags)
    
        if 'ORDERTRACKS' in song.tags.keys() and not ignore_stamp:
            if verbose: print("File already modified.")
            continue
    
    
        track_number = get_track_number(song)
            
        disc_letter = get_disc_letter(song)
                            
        title = get_title(song)
            
        if  disc_letter or track_number:
            
            new_title = disc_letter+track_number+'- '+title
                
            if verbose: 
                print("Old title:",title)
                print("New title:",new_title)
                    
            song.tags["TITLE"] = [new_title]
            song.tags["ORDERTRACKS"] = ['Y']
            if do_save: 
                modified+=1
                song.save()
        else:
            if verbose: print("Title not modified as not DISC or TRACK number found.")

if verbose: 
    print("Total files procesed:", count)
    print("Total files modified:", modified)
        
            