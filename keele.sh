#!/usr/bin/env sh

# download archive files:
wget --recursive --level 1 --no-directories \
     --accept "*.pel" --accept "*.pes" --accept "*.pet" --accept "*.pev" \
     --accept keele_pitch_database.htm --accept read.me \
     https://lost-contact.mit.edu/afs/nada.kth.se/dept/tmh/corpora/KeelePitchDB/Speech/

mkdir -p KEELE_orig
mv *.pel *.pes *.pet *.pev keele_pitch_database.htm read.me KEELE_orig
rm robots.txt.tmp
