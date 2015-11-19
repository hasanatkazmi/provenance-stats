#!/usr/bin/env bash

# Make sure coreutils.sh is executed before this script.
# This script assumes that coreutils binaries are already built.

BASEDIR=$(dirname $0)
cwd=$(pwd)
cd $BASEDIR/../../staging/coreutils-8.24/src


for bin in cat ls
do
	$BASEDIR/../../staging/whole-program-llvm/extract-bc $bin
	$BASEDIR/../../staging/SPADE/bin/llvm/llvmTrace.sh $bin  -no-monitor $bin -instrument-libc
done

cd $cwd
