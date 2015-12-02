#!/usr/bin/env bash

# Make sure coreutils.sh is executed before this script.
# This script assumes that coreutils binaries are already built.

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cwd=$(pwd)
cd $BASEDIR/../../staging/coreutils-8.24/src

PATH=$PATH:$(realpath $BASEDIR/../../staging/whole-program-llvm)
export PATH

for bin in cat cp dd base64 cksum comm csplit cut expand fmt fold head join md5sum nl od paste pr ptx sha1sum sha224sum sha256sum sha384sum sha512sum shuf sort split sum tac tail tee tr truncate tsort unexpand uniq wc
do
	extract-bc $bin
	$(realpath $BASEDIR/../../staging/SPADE/bin/llvm/llvmTrace.sh) $bin -no-monitor $bin -instrument-libc
done

cd $cwd

mkdir -p $BASEDIR/../../bins/instrumented/
cp -r $BASEDIR/../../staging/coreutils-8.24 $BASEDIR/../../bins/instrumented/coreutils-8.24
