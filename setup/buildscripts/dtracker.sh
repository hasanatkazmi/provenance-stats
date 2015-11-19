#!/usr/bin/env sh

BASEDIR=$(dirname $0)
cwd=$(pwd)
DTRACKER_HOME=$BASEDIR/../../staging/dtracker

cd $DTRACKER_HOME

# Pin only works on 32 bit Linux. 

make -C support -f makefile.pin
make -C support -f makefile.provtoolbox

export PIN_HOME="$DTRACKER_HOME"/pin
make support-libdft
make

cd $cwd
