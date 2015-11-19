#!/usr/bin/env bash

# Make sure coreutils.sh is executed before this script.
# This script assumes that coreutils binaries are already built.

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cwd=$(pwd)
cd $BASEDIR/../../staging/coreutils-8.24/src

PATH=$PATH:$(realpath $BASEDIR/../../staging/whole-program-llvm)
export PATH

for bin in cat
do
	extract-bc $bin
	$(realpath $BASEDIR/../../staging/SPADE/bin/llvm/llvmTrace.sh) $bin -no-monitor $bin -instrument-libc
done

cd $cwd
