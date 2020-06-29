#!/usr/bin/env sh

wget https://www2.spsc.tugraz.at/databases/PTDB-TUG/SPEECH_DATA_ZIPPED.zip
wget https://www2.spsc.tugraz.at/databases/PTDB-TUG/DOCUMENTATION/RECORDING-PROTOCOL.txt
wget https://www2.spsc.tugraz.at/databases/PTDB-TUG/DOCUMENTATION/SPEAKER-PROFILES.txt
wget https://www2.spsc.tugraz.at/databases/PTDB-TUG/DOCUMENTATION/TIMIT-PROMPTS.txt

unzip SPEECH_DATA_ZIPPED.zip -d PTDB_TUG_orig
mv RECORDING-PROTOCOL.txt SPEAKER-PROFILES.txt TIMIT-PROMPTS.txt PTDB_TUG_orig
rm SPEECH_DATA_ZIPPED.zip
