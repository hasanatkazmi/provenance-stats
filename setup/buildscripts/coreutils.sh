#!/usr/bin/env sh

cwd=$(pwd)
cd $1

export LLVM_COMPILER=clang
export WLLVM_CONFIGURE_ONLY=1
CC=wllvm ./configure 
unset WLLVM_CONFIGURE_ONLY
make

cd $cwd
