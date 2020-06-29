#!/usr/bin/env sh

# download archive files:
wget --recursive --level 1 --accept "*.bz2" --no-directories http://festvox.org/cmu_arctic/packed/
wget http://www.festvox.org/cmu_arctic/index.html

# extract archives
mkdir -p CMU_Arctic_orig
mv index.html CMU_Arctic_orig/CMU_Arctic_Databases.html
for file in cmu_us_*_arctic.tar.bz2
do
    tar --one-top-level=CMU_Arctic_orig -xf "$file"
done

rm robots.txt.tmp cmu_us_*_arctic.tar.bz2
