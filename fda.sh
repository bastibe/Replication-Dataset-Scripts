#!/usr/bin/env sh

wget http://www.cstr.ed.ac.uk/research/projects/fda/fda_eval.tar.gz
tar --one-top-level=FDA_orig -xf fda_eval.tar.gz
rm fda_eval.tar.gz
