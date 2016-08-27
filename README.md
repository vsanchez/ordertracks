# ordertracks
Scans ID3 tags of music files and then changes the title of the track to represent its order within an album... needed for systems that diregard track numbers and simply alphabetize songs.

Some MP3 players (in my case, my Pioneer car player) when listing the tracks within an album will order the tracks by their names, disregarding the track and disc numebers. That is a real problem for audio books, classical music and simply when one wants to hear an Album in the order that the musician organized it. 

What this simple program does is scan a directory and its subdirectory finding music files (at this time only MP3 files) and reading the ID tag to find the the DISCNUMBER and TRACKNUMBER (if available) and then prepending to the song name the Disc (via a letter) and the track number so that the player will order them correctly.

For example, if the song "Hello" is in the second CD, third track then it will be renamed: "B03- Hello". The first letter indicates the number of the DISCNUMBER (coded A, B, C, ... etc) and the 2 digits the order within that disc. If no disc number is found then the letter is dropped.

The program adds a tag to the file so we can use it repeatdly and only do the file once.

THE IDEA IS THAT YOU USE THE PROGRAM ON THE USB DEVICE YOU ARE USING IN THE PLAYER. IT IS NOT RECOMENDED IN YOUR MAIN MUSIC COLLECTION!!!! USE AT YOUR ONW RISK ON YOUR COLLECTION!!

