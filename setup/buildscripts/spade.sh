#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PATH=$PATH:$BASEDIR/../../staging/whole-program-llvm
cwd=$(pwd)
cd $BASEDIR/../../staging/SPADE

git checkout 07ae99c4b4a9a25618f608881b12aa4119ecf329  src/spade/reporter/Strace.java 

./configure
make
make build-linux-llvm

cd $cwd
