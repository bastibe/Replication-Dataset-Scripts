#!/usr/bin/env sh

wget --recursive --level 1 --accept "*.mat" --no-directories http://spib.linse.ufsc.br/noise.html
wget http://spib.linse.ufsc.br/noise.html

mkdir -p NOISEX92_orig
mv *.mat noise.html NOISEX92_orig/
