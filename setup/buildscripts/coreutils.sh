#!/usr/bin/env bash

BASEDIR=$(dirname $0)

cwd=$(pwd)
cd $BASEDIR/../../staging/coreutils-8.24

./configure
make

cd $cwd

mkdir -p $BASEDIR/../../bins/uninstrumented/
cp -r $BASEDIR/../../staging/coreutils-8.24 $BASEDIR/../../bins/uninstrumented/coreutils-8.24
