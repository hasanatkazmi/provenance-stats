#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PATH=$PATH:$BASEDIR/../../staging/whole-program-llvm
cwd=$(pwd)
cd $BASEDIR/../../staging/SPADE

./configure
make
make build-linux-llvm

cd $cwd
