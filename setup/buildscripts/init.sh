#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

bash $BASEDIR/dtracker.sh
bash $BASEDIR/spade.sh
bash $BASEDIR/coreutils.sh
bash $BASEDIR/coreutils-instrumented.sh

cd $BASHDIR/../
