#!/usr/bin/env sh

cwd=$(pwd)
cd $1

./configure
make
make build-linux-llvm

cd $cwd
