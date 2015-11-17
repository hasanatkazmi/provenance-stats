#!/usr/bin/env sh

# Pin only works on 32 bit Linux. 

cwd=$(pwd)
cd $1

DTRACKER_HOME="$HOME"/dtracker

make -C support -f makefile.pin
make -C support -f makefile.provtoolbox

export PIN_HOME="$DTRACKER_HOME"/pin
make support-libdft
make

cd $cwd
