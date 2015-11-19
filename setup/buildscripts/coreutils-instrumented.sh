#!/usr/bin/env bash

# Make sure coreutils.sh is executed before this script.
# This script assumes that coreutils binaries are already built.

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cwd=$(pwd)
cd $BASEDIR/../../staging/coreutils-8.24/src
# cd $BASEDIR/../../staging/whole-program-llvm/

BC=$(readlink -f $BASEDIR/../../../staging/whole-program-llvm/extract-bc)
echo $BC

# for bin in cat ls
# do
# 	# $BASEDIR/../../staging/whole-program-llvm/extract-bc $bin
# 	# $BASEDIR/../../staging/whole-program-llvm/extract-bc

# 	# /home/hasanat/provenance-stats/staging/whole-program-llvm/extract-bc

# 	# $BASEDIR/../../staging/SPADE/bin/llvm/llvmTrace.sh $bin  -no-monitor $bin -instrument-libc
# done

cd $cwd
