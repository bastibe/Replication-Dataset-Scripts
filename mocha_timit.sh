#!/usr/bin/env sh

# download archive files (no recursive downloading, because robots.txt prohibits it):
wget http://data.cstr.ed.ac.uk/mocha/LICENCE.txt
wget http://data.cstr.ed.ac.uk/mocha/README.fsew0.v1.1
wget http://data.cstr.ed.ac.uk/mocha/README.maps0
wget http://data.cstr.ed.ac.uk/mocha/README.msak0
wget http://data.cstr.ed.ac.uk/mocha/README_v1.2.txt
wget http://data.cstr.ed.ac.uk/mocha/fsew0_v1.1.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/maps0.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/mocha-timit.txt
wget http://data.cstr.ed.ac.uk/mocha/msak0_v1.1.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/unchecked/faet0.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/unchecked/falh0.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/unchecked/ffes0.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/unchecked/fjmw0.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/unchecked/mjjn0.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/unchecked/mkxr0.tar.gz
wget http://data.cstr.ed.ac.uk/mocha/unchecked/ss240402.tar.gz


for file in *.tar.gz
do
    tar --one-top-level=MOCHA_TIMIT_orig/$(basename "$file" .tar.gz)/ -xf "$file"
done

mv README* LICENCE.txt mocha-timit.txt MOCHA_TIMIT_orig/

# move files with inconsistent names to their correct positions:
mv MOCHA_TIMIT_orig/mkxr0/mkxr0/* MOCHA_TIMIT_orig/mkxr0/
mv MOCHA_TIMIT_orig/ss240402/ss240402/* MOCHA_TIMIT_orig/ss240402/

rm *.tar.gz
