#!/usr/bin/env bash

BASEDIR=$(dirname $0)

bash $BASEDIR/dtracker.sh
bash $BASEDIR/spade.sh
bash $BASEDIR/coreutils.sh
bash $BASEDIR/coreutils-instrumented.sh
