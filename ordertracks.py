#!/usr/bin/python3

import sys
import os
import taglib

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
            if int(track_number) < 10:
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

narguments = len(sys.argv)
if narguments != 2:
    print("erro: ordertracks.py path")
    exit(1);
    
print('Argument List:', str(sys.argv))
rootdir = str(sys.argv[1])

count = 0
for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".mp3"):
            musicfile = os.path.join(root, file)
            
            count= count+1
            song = taglib.File(musicfile)
            print(musicfile)
            print(song.tags)
            
            track_number = get_track_number(song)
            
            disc_letter = get_disc_letter(song)
                            
            title = get_title(song)
            
            if  disc_letter or track_number:
                new_title = disc_letter+track_number+'- '+title
                print(new_title)
                song.tags["TITLE"] = [new_title]
                song.tags["ORDERTRACKS"] = ['Y']
                song.save()
    print(count)
            