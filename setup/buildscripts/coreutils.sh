#!/usr/bin/env bash

BASEDIR=$(dirname $0)

cwd=$(pwd)
cd $BASEDIR/../../staging/coreutils-8.24

PATH=$PATH:$BASEDIR/../../staging/whole-program-llvm
export $PATH

#./configure
#make
export LLVM_COMPILER=clang
export WLLVM_CONFIGURE_ONLY=1
CC=wllvm ./configure 
unset WLLVM_CONFIGURE_ONLY
make

cd $cwd

mkdir -p $BASEDIR/../../bins/uninstrumented/
cp -r $BASEDIR/../../staging/coreutils-8.24 $BASEDIR/../../bins/uninstrumented/coreutils-8.24
