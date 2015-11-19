#!/usr/bin/env bash

BASEDIR=$(dirname $0)
PATH=$PATH:$BASEDIR/../../staging/whole-program-llvm
cwd=$(pwd)
cd $BASEDIR/../../staging/SPADE

./configure
make
make build-linux-llvm

cd $cwd
