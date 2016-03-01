#!/usr/bin/env sh

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cwd=$(pwd)
DTRACKER_HOME=$BASEDIR/../../staging/dtracker

cd $DTRACKER_HOME

# Pin only works on 32 bit Linux. 

make -C support -f makefile.pin
make -C support -f makefile.provtoolbox

export PIN_HOME="$DTRACKER_HOME"/pin
cd support
git clone https://github.com/m000/byte-unixbench.git
cd ..
GIT_SSL_NO_VERIFY=true git submodule update --init
make support-libdft
make

cd $cwd
