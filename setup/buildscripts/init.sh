#!/bin/bash

BASEDIR=$(dirname $0)

sh $BASEDIR/coreutils.sh $BASEDIR/../../staging/coreutils-*
sh $BASEDIR/spade.sh $BASEDIR/../../staging/SPADE/
sh $BASEDIR/dtracker.sh $BASEDIR/../../staging/dtracker/

