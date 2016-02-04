#!/usr/bin/env bash

# Make sure coreutils.sh is executed before this script.
# This script assumes that coreutils binaries are already built.

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cwd=$(pwd)
cd $BASEDIR/../../staging/coreutils-8.24/src

PATH=$PATH:$(realpath $BASEDIR/../../staging/whole-program-llvm)
export PATH
export LLVM_COMPILER=clang

# extract-bc for null will fail in the loop after this, but we already have extracted bc here. (we havnt compiled it using whole-prgtram-llvm so extrac-bc will fail on null)
$LLVM_COMPILER -emit-llvm null.c -c -o null.bc

for bin in cat cp dd base64 cksum comm csplit cut expand fmt fold head join md5sum nl od paste pr ptx sha1sum sha224sum sha256sum sha384sum sha512sum shuf sort split sum tac tail tee tr truncate tsort unexpand uniq wc null
do
	extract-bc $bin
	$(realpath $BASEDIR/../../staging/SPADE/bin/llvm/llvmTrace.sh) $bin -no-monitor $bin -instrument-libc
done

cd $cwd

mkdir -p $BASEDIR/../../bins/instrumented/
cp -r $BASEDIR/../../staging/coreutils-8.24 $BASEDIR/../../bins/instrumented/coreutils-8.24
